# MovieLens Recommendation Backend

This backend loads `../model/movielens_recommender.pkl` and exposes a small Netflix-style recommendation API.

## Run

```powershell
cd $env:USERPROFILE\OneDrive\Desktop\Movielens
python train_export_model.py
python backend\app.py
```

## Endpoints

Health check:

```text
GET http://127.0.0.1:5000/health
```

Search movies:

```text
GET http://127.0.0.1:5000/movies/search?q=matrix
```

Recommend from watched movies:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:5000/recommend `
  -ContentType 'application/json' `
  -Body '{"titles":["matrix","dark knight","inception"],"top_n":10}'
```

You can also pass `movie_ids`, for example:

```json
{
  "movie_ids": [2571, 58559, 79132],
  "top_n": 10
}
```
