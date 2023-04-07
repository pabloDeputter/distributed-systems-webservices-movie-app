<script setup lang="ts">
import {
  fetchRequest,
  getImageSource,
  deleteMovie,
  getRecommendations,
  getFavoriteMovies,
  contains,
} from "@/utils/utils";
import { useRoute } from "vue-router";
import Loading from "@/components/LoadingComponent.vue";
import { onMounted, provide, ref, watchEffect, type Ref } from "vue";
import type { RecommendationType } from "@/types/types";
import MovieTable from "@/components/MovieTable.vue";
import RecommendationsSelector from "@/components/RecommendationsSelector.vue";
const loading = ref(true);
const details: Ref<any> = ref(null);
const route = useRoute();
const movieID = ref(Number(useRoute().params["id"]));
const favoriteMovies = ref([]);

/**
 * Lifecycle hook that is called after the component has mounted.
 */
onMounted(async () => {
  const response = await fetchRequest(
    `http://127.0.0.1:5000/api/movie/${movieID.value}`
  );

  details.value = response;
  loading.value = false;
  getRecommendations(
    movieID.value,
    selectedRecommendation,
    similarMovies,
    loadingRecommendations,
    error
  );

  // Check if user is logged in.
  if (isLoggedIn()) {
    const details = await fetchRequest(
      `http://127.0.0.1:5000/api/account?session_id=${sessionStorage.getItem(
        "session_id"
      )}`
    );
    // Retrieve favorite movies.
    const response = await getFavoriteMovies(details["data"]["id"]);
    favoriteMovies.value = response["data"]["results"];
    isFavorite.value = contains(favoriteMovies.value, movieID.value);
  }
});

/**
 * Checks whether the user is logged in.
 */
const isLoggedIn = () => {
  return sessionStorage.getItem("session_id") !== null;
};

/**
 * Sends a request to mark the current movie as a favorite for the logged-in user.
 */
const onFavorite = async () => {
  isFavorite.value = !isFavorite.value;
  // First retrieve account details for ID.
  const accountDetails = await fetchRequest(
    `http://127.0.0.1:5000/api/account?session_id=${sessionStorage.getItem(
      "session_id"
    )}`,
    "GET"
  );
  await fetchRequest(
    `http://127.0.0.1:5000/api/account/${
      accountDetails["data"]["id"]
    }/favorite?session_id=${sessionStorage.getItem("session_id")}`,
    "POST",
    {
      media_type: "movie",
      media_id: details.value["id"],
      favorite: isFavorite.value,
    }
  );
};

/** Indicates if it is loading */
const loadingRecommendations = ref<boolean>(false);
/** Indicates errors */
const error = ref<string>("");
// Holds the selected recommendations
const selectedRecommendation = ref<RecommendationType>("Exact genre");
// Provide this reactive object to children components.
provide("selectedRecommendation", selectedRecommendation);
// Holds the query typing timeout.
const queryTimeout = ref<any | null>(null);

/** Holds the list of similar movies. */
const similarMovies = ref([]);

const isFavorite = ref(false);

// Will be executed whenever the movieID value changes.
const onChange = () => {
  clearTimeout(queryTimeout.value);
  queryTimeout.value = setTimeout(async () => {
    getRecommendations(
      movieID.value,
      selectedRecommendation,
      similarMovies,
      loadingRecommendations,
      error
    );
  }, 250);
};

// Executed when the route parameter in this case movieID changes value.
watchEffect(async () => {
  loading.value = true;
  movieID.value = Number(route.params["id"]);
  const response = await fetchRequest(
    `http://127.0.0.1:5000/api/movie/${movieID.value}`
  );
  error.value = "";
  selectedRecommendation.value = "Exact genre";
  getRecommendations(
    movieID.value,
    selectedRecommendation,
    similarMovies,
    loadingRecommendations,
    error
  );
  details.value = response;
  loading.value = false;
});
</script>
<template>
  <div class="mt-4 grid grid-cols-1 gap-5">
    <Loading class="col-span-1" v-if="loading" />
    <div v-else class="col-span-1 flex rounded-lg shadow-2xl">
      <div class="relative w-48 flex-none">
        <img
          :src="getImageSource(details)"
          class="absolute inset-0 h-full w-full rounded-lg object-cover"
        />
      </div>
      <form class="flex-auto p-6">
        <div class="flex flex-wrap">
          <h1 class="dark:text-gray-50 flex-auto text-xl font-semibold">
            {{ details["original_title"] }} ({{ details["release_date"] }})
          </h1>
          <div class="flex items-center justify-center gap-4">
            <svg
              v-show="isLoggedIn()"
              class="w-6 cursor-pointer fill-red-600"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 512 512"
              @click="onFavorite()"
              :class="isFavorite ? 'opacity-100' : 'opacity-40'"
            >
              <!--! Font Awesome Pro 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
              <path
                d="M47.6 300.4L228.3 469.1c7.5 7 17.4 10.9 27.7 10.9s20.2-3.9 27.7-10.9L464.4 300.4c30.4-28.3 47.6-68 47.6-109.5v-5.8c0-69.9-50.5-129.5-119.4-141C347 36.5 300.6 51.4 268 84L256 96 244 84c-32.6-32.6-79-47.5-124.6-39.9C50.5 55.6 0 115.2 0 185.1v5.8c0 41.5 17.2 81.2 47.6 109.5z"
              />
            </svg>
            <svg
              class="w-5 cursor-pointer fill-white"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 448 512"
              @click="deleteMovie(details['id'])"
            >
              <!--! Font Awesome Pro 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
              <path
                d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"
              />
            </svg>
          </div>
          <div class="flex w-full gap-x-1 text-sm font-medium opacity-70">
            <div v-for="(genre, index) in details['genres']" :key="index">
              {{ genre["name"] }} -
            </div>
            {{ details["runtime"] }} min
          </div>
          <div class="mt-2 w-full flex-none text-sm font-medium">
            <div class="text-base">Overview</div>
            {{ details["overview"] }}
          </div>
        </div>
        <div class="flex items-center justify-end gap-x-2">
          <svg
            class="w-4 fill-yellow-400"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 576 512"
          >
            <!--! Font Awesome Pro 6.3.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
            <path
              d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"
            />
          </svg>
          {{ details["vote_average"] }}
        </div>
      </form>
    </div>
    <div v-if="!loading" class="col-span-1">
      <RecommendationsSelector @input="onChange()" />
    </div>
    <div v-if="!loading" class="col-span-1">
      <progress
        v-if="loadingRecommendations"
        class="progress w-full"
      ></progress>
      <h1
        class="flex items-center justify-center font-medium"
        v-if="!loadingRecommendations && error !== ''"
      >
        {{ error }}
      </h1>
      <MovieTable
        v-if="!loadingRecommendations"
        :similarMovies="similarMovies"
      />
    </div>
  </div>
</template>
