<script setup lang="ts">
import { ref, onMounted } from "vue";
import type { Ref } from "vue";
import { fetchRequest, deleteMovie, getImageSource } from "@/utils/utils";
import Loading from "@/components/LoadingComponent.vue";
import MovieCard from "@/components/MovieCard.vue";

/** Number of popular movies to be fetched, default is 10. */
const movieCount = ref(10);
// Holds the query typing timeout.
const queryTimeout: Ref<any | null> = ref(null);
/** Holds the list of popular movies. */
const popularMovies = ref([]);
/** Loading */
const loading = ref(true);

/** Fetch n popular movies from the API. */
const getPopular = async (n: number) => {
  const response = await fetchRequest(
    `http://127.0.0.1:5000/api/movie/top-movies/${n}`
  );
  return response;
};

/**
 * Executed when component mounts.
 */
onMounted(async () => {
  const response = await getPopular(movieCount.value);
  popularMovies.value = response["data"]["results"];
  loading.value = false;
});

/**
 * Executed when typing.
 */
const search = () => {
  // Clear previously set timeout.
  clearTimeout(queryTimeout.value);
  // Reset data.
  queryTimeout.value = setTimeout(async () => {
    if (movieCount.value !== 0) {
      loading.value = true;
      const response = await getPopular(movieCount.value);
      popularMovies.value = response["data"]["results"];
      loading.value = false;
    }
  }, 750);
};

/**
 * Delete a movie by ID.
 * @param {number} id - Id of movie to be deleted
 */
const onDelete = async (id: number) => {
  loading.value = true;
  await deleteMovie(id);
  const response = await getPopular(movieCount.value);
  popularMovies.value = response["data"]["results"];
  loading.value = false;
};
</script>

<template>
  <div class="grid grid-cols-4 gap-10">
    <div class="form-control col-span-4 w-full max-w-xs lg:col-span-1">
      <label class="label">
        <span class="label-text">Amount of popular movies:</span>
      </label>
      <input
        v-model="movieCount"
        :min="0"
        type="number"
        placeholder="Enter a number..."
        class="input-bordered input w-full max-w-xs"
        @change="search()"
      />
    </div>
    <div class="col-span-4 w-full items-center justify-center" v-if="loading">
      <Loading />
    </div>
    <MovieCard
      v-else
      v-for="(movie, index) in popularMovies"
      :key="index"
      :title="movie['original_title']"
      :id="movie['id']"
      :rating="movie['vote_average']"
      :image="getImageSource(movie)"
      @movieDelete="onDelete"
      @movieDetails="
        (e) => {
          $router.push(`/movie/${e}`);
        }
      "
    />
  </div>
</template>
