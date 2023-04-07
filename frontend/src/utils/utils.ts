import type { Ref } from "vue";
import type { RecommendationType } from "../types/types";

// Generic fetch function.
export function fetchRequest(
  url: string,
  method: string = "GET",
  data: any = {}
): Promise<any> {
  const promise = fetch(url, {
    method: method,
    mode: "cors",
    ...(method !== "GET" && {
      body: JSON.stringify(data),
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
        "Access-Control-Allow-Headers":
          "Content-Type, Authorization, X-Requested-With, Origin",
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
    }),
  })
    .then((response) => response.json())
    .then((data: any) => data);
  promise.catch((error) => console.error(error));
  return promise;
}

/**
 * Delete a movie by id.
 * @param {number} id - ID of movie to be deleted
 */
export const deleteMovie = async (id: number) => {
  const promise = await fetch(`http://127.0.0.1:5000/api/movie/${id}`, {
    method: "DELETE",
  });
  return promise;
};

/**
 * Get image for movie
 * @param {any} movie - movie
 */
export const getImageSource = (movie: any) => {
  return `https://image.tmdb.org/t/p/original/${movie["backdrop_path"]}`;
};

/**
 * Get recommendations for selected movie and recommendation type.
 * @param {number} movie - Movie ID
 * @param {Ref<RecommendationType>} selectedRecommendation - Selected recommendation type
 * @param {Ref<any[]>} similarMovies - List of similar movies
 * @param {Ref<boolean>} loading - Indicates whether request is still loading
 * @param {Ref<string>} error - Indicates whether there is an error
 * @param {number} page - Page number
 */
export const getRecommendations = async (
  movie: number,
  selectedRecommendation: Ref<RecommendationType>,
  similarMovies: Ref<any[]>,
  loading: Ref<boolean>,
  error: Ref<string>,
  page: number = 1
) => {
  // Return if movie ID is not defined or no recommendation type is selected.
  if (movie === undefined || !selectedRecommendation.value) {
    return;
  }
  // Reset values.
  loading.value = true;
  similarMovies.value = [];
  error.value = "";

  // Get the correct API endpoint depending on the selected recommendation type value.
  const recommendationType: string =
    selectedRecommendation.value === "Exact genre"
      ? "similar-genre"
      : selectedRecommendation.value === "Similar runtime (+- 10 mins)"
      ? "similar-runtime"
      : "overlapping-actors";

  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/movie/${recommendationType}/${movie}?page=${page}`
    );
    const data = await response.json();

    if (response.ok) {
      similarMovies.value = data["data"].results;
    } else {
      console.error(
        `Failed to fetch similar movies: ${response.status} ${response.statusText}`
      );
      error.value = `Failed to fetch similar movies: ${response.status} ${response.statusText}`;
    }
  } catch (error) {
    console.error(`Failed to fetch similar movies: ${error}`);
  }

  loading.value = false;
};

/**
 * Retrieve favorite movies.
 * @param {number} id - Account ID
 */
export const getFavoriteMovies = async (id: number) => {
  // Retrieve favorite movies.
  const response = await fetchRequest(
    `http://127.0.0.1:5000/api/account/${id}/favorite/movies?session_id=${sessionStorage.getItem(
      "session_id"
    )}`
  );
  return response;
};

/**
 * Check if list contains given ID.
 * @param {any[]} list - List
 * @param {number} id - ID we want to search for
 */
export const contains = (list: any[], id: number) => {
  if (list.filter((e) => Number(e.id) === Number(id)).length > 0) {
    return true;
  }
  return false;
};
