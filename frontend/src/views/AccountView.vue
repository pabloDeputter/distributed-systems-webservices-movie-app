<script setup lang="ts">
import { fetchRequest, getFavoriteMovies } from "@/utils/utils";
import { onMounted, ref } from "vue";
import MovieTable from "@/components/MovieTable.vue";
import Loading from "@/components/LoadingComponent.vue";

const loading = ref<boolean>(true);
// Holds details of user.
const details = ref<any>({});
// Holds favorites of user.
const favorites = ref<any[]>([]);

// Executed when component mounts.
onMounted(async () => {
  const response = await fetchRequest(
    `http://127.0.0.1:5000/api/account?session_id=${sessionStorage.getItem(
      "session_id"
    )}`,
    "GET"
  );
  details.value = response["data"];
  const a = await getFavoriteMovies(details.value["id"]);
  favorites.value = a["data"]["results"];
  loading.value = false;
});
</script>

<template>
  <div class="mt-4 grid grid-cols-2">
    <div class="col-span-2">
      <Loading v-if="loading" />
      <MovieTable v-else :similar-movies="favorites" :showPage="false" />
    </div>
  </div>
</template>
