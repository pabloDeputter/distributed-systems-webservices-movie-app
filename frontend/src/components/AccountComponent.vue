<script setup lang="ts">
import { inject, ref, onMounted } from "vue";

// Retrieve functions provided by higher-level components.
const onLogin = inject("onLogin") as Function;
const onLogout = inject("onLogout") as Function;

// Holds whether user is logged in.
const loggedIn = ref(
  sessionStorage.getItem("session_id") === null ? false : true
);

// Executed when component mounts.
onMounted(() => {
  window.addEventListener(
    "session-id-session-storage-changed",
    (event: any) => {
      loggedIn.value = event.detail.storage;
    }
  );
});
</script>

<template>
  <div class="dropdown dropdown-end">
    <label tabindex="0" class="btn-ghost btn-circle avatar btn">
      <div class="w-10 rounded-full">
        <img
          src="https://i.etsystatic.com/5902969/r/il/0f9a5c/1423351994/il_1080xN.1423351994_a2yz.jpg"
        />
      </div>
    </label>
    <ul
      tabindex="0"
      class="dropdown-content menu rounded-box menu-compact mt-3 w-52 bg-base-100 p-2 shadow"
    >
      <li v-show="loggedIn">
        <RouterLink :to="'/account'">
          <a class="">Account</a>
        </RouterLink>
      </li>
      <li v-show="!loggedIn"><a @click="onLogin()">Login</a></li>
      <li v-show="loggedIn">
        <a @click="onLogout()">Logout</a>
      </li>
    </ul>
  </div>
</template>
