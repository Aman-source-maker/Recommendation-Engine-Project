from pathlib import Path
import pickle

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "ml-latest-small"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "movielens_recommender.pkl"


def build_model():
    ratings = pd.read_csv(DATA_DIR / "ratings.csv")
    movies = pd.read_csv(DATA_DIR / "movies.csv")

    movie_stats = ratings.groupby("movieId").agg(
        rating_count=("rating", "count"),
        rating_mean=("rating", "mean"),
    ).reset_index()

    movies = movies.merge(movie_stats, on="movieId", how="left")
    movies["rating_count"] = movies["rating_count"].fillna(0).astype(int)
    movies["rating_mean"] = movies["rating_mean"].fillna(0.0)

    user_codes, user_ids = pd.factorize(ratings["userId"], sort=True)
    movie_codes, movie_ids = pd.factorize(ratings["movieId"], sort=True)

    # Center ratings by each user's average to compare taste patterns, not rating generosity.
    user_means = ratings.groupby("userId")["rating"].mean().reindex(user_ids).to_numpy()
    centered_ratings = ratings["rating"].to_numpy(dtype=np.float32) - user_means[user_codes]

    item_user_matrix = csr_matrix(
        (centered_ratings, (movie_codes, user_codes)),
        shape=(len(movie_ids), len(user_ids)),
        dtype=np.float32,
    )

    nearest_neighbors = NearestNeighbors(metric="cosine", algorithm="brute")
    nearest_neighbors.fit(item_user_matrix)

    artifact = {
        "model_type": "item_item_cosine_knn",
        "nearest_neighbors": nearest_neighbors,
        "item_user_matrix": item_user_matrix,
        "movie_ids": movie_ids.astype(int),
        "movie_id_to_index": {int(movie_id): int(index) for index, movie_id in enumerate(movie_ids)},
        "movies": movies,
        "ratings_count": int(len(ratings)),
        "users_count": int(ratings["userId"].nunique()),
        "movies_count": int(movies["movieId"].nunique()),
    }

    MODEL_DIR.mkdir(exist_ok=True)
    with MODEL_PATH.open("wb") as model_file:
        pickle.dump(artifact, model_file)

    return artifact


if __name__ == "__main__":
    model = build_model()
    print(f"Exported model: {MODEL_PATH}")
    print(f"Ratings: {model['ratings_count']:,}")
    print(f"Users: {model['users_count']:,}")
    print(f"Movies: {model['movies_count']:,}")
