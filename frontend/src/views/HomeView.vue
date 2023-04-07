<script setup lang="ts">
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { fetchRequest } from "@/utils/utils";

onMounted(async () => {
  const queries: any = useRoute().query;

  if (
    Object.prototype.hasOwnProperty.call(queries, "request_token") &&
    queries["approved"]
  ) {
    const response = await fetchRequest(
      `http://127.0.0.1:5000/api/authentication/session`,
      "POST",
      {
        request_token: queries["request_token"],
      }
    );
    if (response["data"]["success"]) {
      sessionStorage["session_id"] = response["data"]["session_id"];
      // Dispatch event that session_id has changed.
      window.dispatchEvent(
        new CustomEvent("session-id-session-storage-changed", {
          detail: {
            storage: true,
          },
        })
      );
    }
  }
});
</script>

<template>
  <div>home</div>
</template>
