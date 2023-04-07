<script setup lang="ts">
import { inject } from "vue";
const selectedRecommendation = inject("selectedRecommendation");
</script>

<template>
  <div class="form-control w-full max-w-xs">
    <label class="label">
      <span class="label-text">Recommendation type:</span>
    </label>
    <select v-model="selectedRecommendation" class="select-bordered select">
      <option>Exact genre</option>
      <option>Similar runtime (+- 10 mins)</option>
      <option>Overlapping actors</option>
    </select>
  </div>
</template>
