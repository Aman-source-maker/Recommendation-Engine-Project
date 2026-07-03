const API_BASE_URL = "http://127.0.0.1:5000";
const app = document.querySelector("#app");
const homeTemplate = document.querySelector("#homeTemplate");
const watchTemplate = document.querySelector("#watchTemplate");

function cleanTitle(title) {
  return title.replace(/\s*\(\d{4}\)\s*$/, "");
}

function genreText(genres) {
  return String(genres || "").split("|").join(" / ");
}

function findImportedMovie(movieId) {
  return window.IMPORTED_MOVIES.find((movie) => movie.movieId === Number(movieId));
}

function createMovieCard(movie, options = {}) {
  const button = document.createElement("button");
  button.className = options.compact ? "movie-card compact-card" : "movie-card";
  button.type = "button";

  const imported = findImportedMovie(movie.movieId);
  const thumbnail = movie.thumbnail || imported?.thumbnail;

  if (thumbnail) {
    const image = document.createElement("img");
    image.src = thumbnail;
    image.alt = `${movie.title} thumbnail`;
    button.appendChild(image);
  } else {
    const fallback = document.createElement("div");
    fallback.className = "fallback-poster";
    fallback.textContent = cleanTitle(movie.title);
    button.appendChild(fallback);
  }

  const label = document.createElement("span");
  label.textContent = movie.title;
  button.appendChild(label);

  button.addEventListener("click", () => renderWatch(movie));
  return button;
}

function renderHome() {
  const view = homeTemplate.content.cloneNode(true);
  const featured = window.IMPORTED_MOVIES[8];

  view.querySelector("#heroTitle").textContent = cleanTitle(featured.title);
  view.querySelector("#heroMeta").textContent = genreText(featured.genres);
  view.querySelector(".hero-backdrop").style.backgroundImage = `linear-gradient(90deg, rgba(8,8,8,.96) 0%, rgba(8,8,8,.58) 42%, rgba(8,8,8,.16) 100%), url("${featured.thumbnail}")`;
  view.querySelector("#heroPlay").addEventListener("click", () => renderWatch(featured));
  view.querySelector("#heroInfo").addEventListener("click", () => renderWatch(featured));

  const grid = view.querySelector("#movieGrid");
  window.IMPORTED_MOVIES.forEach((movie) => grid.appendChild(createMovieCard(movie)));

  app.replaceChildren(view);
  window.history.replaceState(null, "", "#/");
}

async function fetchRelated(movieId) {
  const response = await fetch(`${API_BASE_URL}/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      movie_ids: [movieId],
      top_n: 10
    })
  });

  if (!response.ok) {
    throw new Error(`Recommendation request failed: ${response.status}`);
  }

  return response.json();
}

async function renderRelated(movie) {
  const grid = document.querySelector("#relatedGrid");
  const status = document.querySelector("#relatedStatus");

  try {
    const payload = await fetchRelated(movie.movieId);
    grid.replaceChildren();

    if (!payload.recommendations.length) {
      status.textContent = "No related movies returned by the model.";
      return;
    }

    status.textContent = "";
    payload.recommendations.forEach((related) => {
      grid.appendChild(createMovieCard(related, { compact: true }));
    });
  } catch (error) {
    status.textContent = "Recommendation backend is not reachable. Start the Flask backend and refresh this page.";
  }
}

function renderWatch(movie) {
  const view = watchTemplate.content.cloneNode(true);
  const imported = findImportedMovie(movie.movieId);
  const poster = movie.thumbnail || imported?.thumbnail;

  view.querySelector("#watchTitle").textContent = cleanTitle(movie.title);
  view.querySelector("#watchGenres").textContent = genreText(movie.genres);
  const posterNode = view.querySelector("#watchPoster");
  if (poster) {
    posterNode.src = poster;
    posterNode.alt = `${movie.title} thumbnail`;
  } else {
    const fallback = document.createElement("div");
    fallback.className = "fallback-poster watch-fallback";
    fallback.textContent = cleanTitle(movie.title);
    posterNode.replaceWith(fallback);
  }
  view.querySelector("#backButton").addEventListener("click", renderHome);

  app.replaceChildren(view);
  window.history.replaceState(null, "", `#/watch/${movie.movieId}`);
  renderRelated(movie);
}

document.querySelector("#homeButton").addEventListener("click", renderHome);
window.addEventListener("load", renderHome);
