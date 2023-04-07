<script setup lang="ts">
import { ref, provide } from "vue";
import { getRecommendations } from "@/utils/utils";
import type { RecommendationType } from "@/types/types";
import RecommendationsSelector from "@/components/RecommendationsSelector.vue";
import MovieTable from "@/components/MovieTable.vue";

/** Movie ID to find similar movies from. */
const movieID = ref<number | undefined>(undefined);
/** Indicates if it is loading */
const loading = ref<boolean>(false);
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

// Will be executed whenever the movieID value changes.
const onChange = (page: number = 1) => {
  clearTimeout(queryTimeout.value);
  queryTimeout.value = setTimeout(async () => {
    getRecommendations(
      movieID.value as number,
      selectedRecommendation,
      similarMovies,
      loading,
      error,
      page
    );
  }, 250);
};
</script>

<template>
  <div class="grid grid-cols-4 gap-10">
    <div class="col-span-2">
      <RecommendationsSelector @input="onChange()" />
    </div>
    <div class="col-span-2">
      <div class="form-control col-span-4 w-full max-w-xs lg:col-span-1">
        <label class="label">
          <span class="label-text">Movie ID:</span>
        </label>
        <input
          :min="0"
          v-model="movieID"
          type="number"
          placeholder="Enter an ID..."
          class="input-bordered input w-full max-w-xs"
          @input="onChange()"
        />
      </div>
    </div>

    <div class="col-span-4 w-full overflow-x-auto">
      <MovieTable
        :similarMovies="similarMovies"
        :showPage="true"
        @pageChange="onChange"
      />
      <progress v-if="loading" class="progress w-full"></progress>
      <h1
        class="flex items-center justify-center font-medium"
        v-if="!loading && error !== ''"
      >
        {{ error }}
      </h1>
    </div>
  </div>
</template>
