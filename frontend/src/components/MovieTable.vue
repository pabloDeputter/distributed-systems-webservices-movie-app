<script setup lang="ts">
import { ref, type Ref } from "vue";
import { getImageSource } from "@/utils/utils";
import { deleteMovie } from "@/utils/utils";
defineProps({
  similarMovies: { required: true },
  showPage: { required: false, default: false },
});
const emit = defineEmits<{
  (e: "pageChange", id: number): void;
}>();

const pageNumber = ref(1);
// Holds the query typing timeout.
const queryTimeout: Ref<any | null> = ref(null);
/**
 * Executed when typing.
 */
const search = () => {
  // Clear previously set timeout.
  clearTimeout(queryTimeout.value);
  // Reset data.
  queryTimeout.value = setTimeout(async () => {
    emit("pageChange", pageNumber.value);
  }, 500);
};
</script>

<template>
  <div>
    <div v-show="showPage" class="form-control mb-2">
      <label class="label">
        <span class="label-text">Page:</span>
      </label>
      <input
        v-model="pageNumber"
        :min="1"
        :max="500"
        type="number"
        placeholder="Enter a number..."
        class="input-bordered input w-full max-w-xs"
        @input="search()"
      />
    </div>
    <table class="table-zebra table w-full">
      <!-- head -->
      <thead>
        <tr>
          <th>Title</th>
          <th>ID</th>
          <th>Average Vote</th>
          <th>Genre's</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in similarMovies" :key="index">
          <td
            class="cursor-pointer"
            @click="$router.push(`/movie/${item['id']}`)"
          >
            <div class="flex items-center space-x-3">
              <div class="avatar">
                <div class="mask mask-squircle h-12 w-12">
                  <img :src="getImageSource(item)" />
                </div>
              </div>
              <div>
                <div class="font-bold">{{ item["original_title"] }}</div>
              </div>
            </div>
          </td>

          <td>{{ item["id"] }}</td>
          <td>{{ item["vote_average"] }}</td>
          <td>{{ item["genre_ids"] }}</td>
          <td>
            <svg
              class="w-4 cursor-pointer fill-white"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 448 512"
              @click="deleteMovie(item['id'])"
            >
              <!--! Font Awesome Pro 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
              <path
                d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"
              />
            </svg>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
