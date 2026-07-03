from pathlib import Path
import pickle

import numpy as np
from flask import Flask, jsonify, request


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "movielens_recommender.pkl"


def load_artifact():
    with MODEL_PATH.open("rb") as model_file:
        artifact = pickle.load(model_file)
    artifact["movies_by_id"] = artifact["movies"].set_index("movieId", drop=False)
    return artifact


artifact = load_artifact()
app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


def movie_record(row):
    return {
        "movieId": int(row["movieId"]),
        "title": row["title"],
        "genres": row["genres"],
        "ratingCount": int(row["rating_count"]),
        "ratingMean": round(float(row["rating_mean"]), 3),
    }


def search_movie_ids(title_queries):
    movie_ids = []
    matches = []
    movies = artifact["movies"]

    for query in title_queries:
        query = str(query).strip().lower()
        if not query:
            continue

        candidates = movies[movies["title"].str.lower().str.contains(query, regex=False, na=False)]
        if candidates.empty:
            continue

        best = candidates.sort_values(["rating_count", "rating_mean"], ascending=False).iloc[0]
        movie_ids.append(int(best["movieId"]))
        matches.append(movie_record(best))

    return movie_ids, matches


def recommend(movie_ids, top_n=10, neighbors_per_seed=50, min_rating_count=20):
    model = artifact["nearest_neighbors"]
    matrix = artifact["item_user_matrix"]
    all_movie_ids = artifact["movie_ids"]
    movie_id_to_index = artifact["movie_id_to_index"]
    movies_by_id = artifact["movies_by_id"]

    seed_ids = [int(movie_id) for movie_id in movie_ids if int(movie_id) in movie_id_to_index]
    if not seed_ids:
        return []

    candidate_scores = {}
    seed_set = set(seed_ids)

    for seed_id in seed_ids:
        seed_index = movie_id_to_index[seed_id]
        distances, indices = model.kneighbors(
            matrix[seed_index],
            n_neighbors=min(neighbors_per_seed + 1, len(all_movie_ids)),
        )

        for distance, candidate_index in zip(distances[0], indices[0]):
            candidate_id = int(all_movie_ids[candidate_index])
            if candidate_id in seed_set:
                continue

            similarity = 1.0 - float(distance)
            if similarity <= 0:
                continue

            current = candidate_scores.setdefault(candidate_id, {"similarities": [], "best_similarity": 0.0})
            current["similarities"].append(similarity)
            current["best_similarity"] = max(current["best_similarity"], similarity)

    recommendations = []
    max_rating_count = max(float(artifact["movies"]["rating_count"].max()), 1.0)

    for candidate_id, score_info in candidate_scores.items():
        row = movies_by_id.loc[candidate_id]
        rating_count = int(row["rating_count"])
        if rating_count < min_rating_count:
            continue

        similarity_score = float(np.mean(score_info["similarities"]))
        quality_score = float(row["rating_mean"]) / 5.0
        popularity_score = np.log1p(rating_count) / np.log1p(max_rating_count)
        score = similarity_score * 0.75 + quality_score * 0.15 + popularity_score * 0.10

        result = movie_record(row)
        result.update({
            "score": round(float(score), 4),
            "similarity": round(float(score_info["best_similarity"]), 4),
        })
        recommendations.append(result)

    recommendations.sort(key=lambda item: item["score"], reverse=True)
    return recommendations[:top_n]


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "modelType": artifact["model_type"],
        "ratings": artifact["ratings_count"],
        "users": artifact["users_count"],
        "movies": artifact["movies_count"],
    })


@app.get("/movies/search")
def search_movies():
    query = request.args.get("q", "")
    limit = min(int(request.args.get("limit", 10)), 50)
    movies = artifact["movies"]
    result = movies[movies["title"].str.lower().str.contains(query.lower(), regex=False, na=False)]
    result = result.sort_values(["rating_count", "rating_mean"], ascending=False).head(limit)
    return jsonify([movie_record(row) for _, row in result.iterrows()])


@app.post("/recommend")
def recommend_movies():
    payload = request.get_json(silent=True) or {}
    movie_ids = payload.get("movie_ids") or []
    title_queries = payload.get("titles") or []
    top_n = min(int(payload.get("top_n", 10)), 50)

    matched_movies = []
    if title_queries:
        matched_ids, matched_movies = search_movie_ids(title_queries)
        movie_ids = list(movie_ids) + matched_ids

    recommendations = recommend(movie_ids, top_n=top_n)
    return jsonify({
        "inputMovieIds": [int(movie_id) for movie_id in movie_ids],
        "matchedMovies": matched_movies,
        "recommendations": recommendations,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
