<script setup lang="ts">
import { ref } from "vue";
import { fetchRequest } from "@/utils/utils";
import MovieTable from "@/components/MovieTable.vue";

/** Movies to rate */
const movies = ref("1422,141,335984,804150,807,550,680");
const loading = ref(false);

/** Fetch scores from the API. */
const getScores = async (movies: string) => {
  movieScores.value = [];
  loading.value = true;
  const response = await fetchRequest(
    `http://127.0.0.1:5000/api/movie/average-scores?movie_ids=${movies}`
  );
  movieScores.value = response["data"]["movies"];
  chartSource.value = response["data"]["chart"];
  loading.value = false;
};

/** Holds the list of scored movies. */
const movieScores = ref([]);
/** Holds source of chart. */
const chartSource = ref("");
</script>

<template>
  <div class="grid grid-cols-4 gap-10">
    <div class="col-span-4">
      <div class="form-control w-full max-w-xs">
        <label class="label">
          <span class="label-text">Movie ID's:</span>
        </label>
        <input
          v-model="movies"
          type="text"
          placeholder="Enter a movies..."
          class="input-bordered input w-full max-w-xs"
        />
        <button v-if="loading" class="loading btn mt-2">loading</button>
        <button v-else class="btn mt-2" @click="getScores(movies)">
          Submit
        </button>
      </div>
    </div>
    <div v-if="!loading" class="col-span-4 mt-3 grid grid-cols-2 gap-4">
      <div class="col-span-2 lg:col-span-1">
        <img v-if="chartSource !== ''" :src="chartSource" />
      </div>
      <div class="col-span-2 lg:col-span-1">
        <MovieTable :similar-movies="movieScores" />
      </div>
    </div>
    <progress v-else class="progress col-span-4 w-full"></progress>
  </div>
</template>
