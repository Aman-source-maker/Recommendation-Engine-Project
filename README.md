# 🎬 MovieLens Recommendation Engine

A Machine Learning-powered Movie Recommendation System built using **Item-Based Collaborative Filtering**, **K-Nearest Neighbors (KNN)**, and **Cosine Similarity**. The application recommends similar movies based on user-selected movies using the MovieLens dataset and serves recommendations through a Flask REST API with an interactive frontend.

---

## 📌 Overview

Finding movies that match a user's interests can be challenging due to the vast number of available options. This project addresses this problem by implementing a recommendation engine that learns relationships between movies based on user rating patterns.

The recommendation model is trained on the **MovieLens Small Dataset**, optimized using sparse matrices, and exposed through a RESTful API built with Flask.

---

## ✨ Features

- 🎯 Item-Based Collaborative Filtering
- 🤖 K-Nearest Neighbors (KNN) Recommendation Model
- 📊 Cosine Similarity for finding similar movies
- ⭐ User Rating Normalization (Mean Centering)
- ⚡ Sparse Matrix Optimization using SciPy
- 💾 Model Serialization using Pickle
- 🔍 Movie Search API
- 🎬 Personalized Movie Recommendation API
- 🌐 Interactive Frontend
- 📈 Popularity and Quality-Aware Recommendation Scoring

---

# 🏗️ System Architecture

```text
                    MovieLens Dataset
                           │
                           ▼
             Load Movies & Ratings Dataset
                           │
                           ▼
             Calculate Movie Statistics
                           │
                           ▼
          Normalize User Ratings (Mean Centering)
                           │
                           ▼
        Create Sparse Item-User Interaction Matrix
                           │
                           ▼
       Train KNN Model using Cosine Similarity
                           │
                           ▼
          Serialize Model using Pickle (.pkl)
                           │
                           ▼
              Flask REST API Backend
                           │
                           ▼
              Interactive Web Frontend
                           │
                           ▼
              Personalized Recommendations
```

---

# 🛠️ Tech Stack

## Programming Language

- Python

## Machine Learning & Data Processing

- Pandas
- NumPy
- SciPy
- Scikit-learn

## Backend

- Flask

## Frontend

- HTML
- CSS
- JavaScript

## Model Storage

- Pickle

## Dataset

- MovieLens Small Dataset

---

# 📂 Project Structure

```
Recommendation-Engine-Project
│
├── backend
│   ├── app.py
│   └── README.md
│
├── frontend
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   ├── movies.js
│   └── assets
│
├── ml-latest-small
│   ├── movies.csv
│   ├── ratings.csv
│   ├── links.csv
│   ├── tags.csv
│   └── README.txt
│
├── model
│   └── movielens_recommender.pkl
│
├── train_export_model.py
├── requirements.txt
├── Movielens_Movie_Recommendation_Engine.ipynb
└── README.md
```

---

# 🧠 Machine Learning Approach

This project implements an **Item-Based Collaborative Filtering Recommendation System**.

### Workflow

1. Load MovieLens ratings and movie metadata.
2. Compute movie statistics including average rating and rating count.
3. Normalize user ratings by subtracting each user's average rating.
4. Construct a sparse Item-User interaction matrix.
5. Train a K-Nearest Neighbors model using Cosine Similarity.
6. Serialize the trained model using Pickle.
7. Serve recommendations through a Flask REST API.

---

# 📊 Recommendation Strategy

The recommendation score is computed by combining three important factors.

| Component | Weight |
|-----------|--------|
| Movie Similarity | **75%** |
| Average Movie Rating | **15%** |
| Movie Popularity | **10%** |

This scoring strategy ensures that recommendations are:

- Highly similar to the selected movie
- Well-rated by users
- Popular enough to avoid obscure recommendations

---

# 🚀 Installation

## Clone the repository

```bash
git clone https://github.com/Aman-source-maker/Recommendation-Engine-Project.git
```

Navigate to the project directory.

```bash
cd Recommendation-Engine-Project
```

Install the required dependencies.

```bash
pip install -r requirements.txt
```

---

# ▶️ Train the Recommendation Model

Run the following command.

```bash
python train_export_model.py
```

This generates the trained recommendation model inside the **model/** directory.

---

# ▶️ Run the Backend

Navigate to the backend directory.

```bash
cd backend
```

Start the Flask server.

```bash
python app.py
```

The backend will run at:

```
http://127.0.0.1:5000
```

---

# ▶️ Run the Frontend

Simply open

```
frontend/index.html
```

or use a local development server.

---

# 📡 API Documentation

## Health Check

### GET

```
/health
```

Example Response

```json
{
  "status": "ok",
  "modelType": "item_item_cosine_knn",
  "ratings": 100836,
  "users": 610,
  "movies": 9724
}
```

---

## Search Movies

### GET

```
/movies/search?q=toy
```

Returns matching movies sorted by popularity and rating.

---

## Get Recommendations

### POST

```
/recommend
```

Example Request

```json
{
  "titles": [
    "Toy Story",
    "Jumanji"
  ],
  "top_n": 10
}
```

Example Response

```json
{
  "recommendations": [
    {
      "title": "GoldenEye (1995)",
      "score": 0.9123,
      "similarity": 0.8932
    }
  ]
}
```

---

# 📊 Model Details

| Component | Implementation |
|-----------|----------------|
| Recommendation Type | Item-Based Collaborative Filtering |
| Machine Learning Algorithm | K-Nearest Neighbors (KNN) |
| Similarity Metric | Cosine Similarity |
| Matrix Representation | SciPy CSR Sparse Matrix |
| Rating Normalization | Mean Centering |
| Backend Framework | Flask |
| Model Serialization | Pickle |
| Dataset | MovieLens Small Dataset |

---

# 📸 Screenshots

Add screenshots of your application here.

Example:

```
screenshots/homepage.png

screenshots/search.png

screenshots/recommendations.png
```

---

# 🔮 Future Improvements

- Hybrid Recommendation System
- Content-Based Filtering
- Deep Learning Recommendation Models
- User Authentication
- User Profiles
- Recommendation History
- TMDB API Integration for Movie Posters
- Genre-Based Filtering
- Cloud Deployment (Render, AWS, Railway)
- Docker Support

---

# 🤝 Contributing

Contributions are welcome.

If you'd like to improve this project:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Submit a Pull Request.

---

# 📜 License

This project is licensed under the MIT License.

---

# 🙏 Acknowledgements

- MovieLens Dataset by GroupLens Research
- Scikit-learn
- Flask
- Pandas
- NumPy
- SciPy

---

# 👨‍💻 Author

**Aman Dubey**

- GitHub: https://github.com/Aman-source-maker
- LinkedIn: *https://www.linkedin.com/in/aman-dubey-598b211b3/*

---

## ⭐ If you found this project useful, please consider giving it a Star on GitHub!
