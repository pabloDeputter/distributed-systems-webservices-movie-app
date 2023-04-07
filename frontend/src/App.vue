<script setup lang="ts">
import { RouterLink, RouterView, useRoute } from "vue-router";
import { fetchRequest } from "./utils/utils";
import { computed, provide } from "vue";
import Account from "@/components/AccountComponent.vue";

// Executed when user logs in.
const onLogin = async () => {
  const response = await fetchRequest(
    `http://127.0.0.1:5000/api/authentication/token/new`
  );
  window.location.replace(
    `https://www.themoviedb.org/authenticate/${response["data"]["request_token"]}?redirect_to=http://localhost:5177/`
  );
};

// Executed when user logs out.
const onLogout = async () => {
  await fetchRequest(
    `http://127.0.0.1:5000/api/authentication/session`,
    "DELETE",
    {
      session_id: sessionStorage.getItem("session_id"),
    }
  );
  // Dispatch event that session_id has changed.
  window.dispatchEvent(
    new CustomEvent("session-id-session-storage-changed", {
      detail: {
        storage: false,
      },
    })
  );
  sessionStorage.removeItem("session_id");
};
// Provide functions to lower-level components.
provide("onLogin", onLogin);
provide("onLogout", onLogout);

// Holds current route and will be updated.
const route = useRoute();
// const path = computed(() => route.fullPath);
</script>

<template>
  <div>
    <div class="navbar sticky top-0 z-50 bg-base-100 drop-shadow-2xl">
      <div class="navbar-start">
        <div class="dropdown">
          <label tabindex="0" class="btn-ghost btn lg:hidden">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h8m-8 6h16"
              />
            </svg>
          </label>
          <ul
            tabindex="0"
            class="dropdown-content menu rounded-box menu-compact mt-3 w-52 bg-base-100 p-2 shadow"
          >
            <li tabindex="0">
              <a>
                Recommendations
                <svg
                  class="fill-current"
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"
                  />
                </svg>
              </a>
              <ul class="p-2">
                <li>
                  <a
                    ><RouterLink :to="'/popular-movies'">
                      Popular Movies
                    </RouterLink></a
                  >
                </li>
                <li>
                  <a
                    ><RouterLink :to="'/similar-movies'">
                      Similar Movies
                    </RouterLink></a
                  >
                </li>
                <li>
                  <a
                    ><RouterLink :to="'/score-movies'">
                      Score Movies
                    </RouterLink></a
                  >
                </li>
              </ul>
            </li>
            <li tabindex="1">
              <a
                href="http://127.0.0.1:5000/docs"
                target="_blank"
                rel="noopener noreferrer"
                >API Documentation</a
              >
            </li>
          </ul>
        </div>
        <RouterLink :to="'/'">
          <a class="btn-ghost btn text-xl normal-case">Movies</a>
        </RouterLink>
      </div>
      <div class="navbar-center hidden lg:flex">
        <ul class="menu menu-horizontal px-1">
          <li tabindex="0">
            <a>
              Recommendations
              <svg
                class="fill-current"
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
              >
                <path
                  d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"
                />
              </svg>
            </a>
            <ul class="p-2">
              <li>
                <a
                  ><RouterLink :to="'/popular-movies'">
                    Popular Movies
                  </RouterLink></a
                >
              </li>
              <li>
                <a
                  ><RouterLink :to="'/similar-movies'">
                    Similar Movies
                  </RouterLink></a
                >
              </li>
              <li>
                <a
                  ><RouterLink :to="'/score-movies'">
                    Score Movies
                  </RouterLink></a
                >
              </li>
            </ul>
          </li>
          <li tabindex="1">
            <a
              href="http://127.0.0.1:5000/docs"
              target="_blank"
              rel="noopener noreferrer"
              >API Documentation</a
            >
          </li>
        </ul>
      </div>
      <div class="navbar-end">
        <Account />
      </div>
    </div>
    <main class="relative m-2">
      <RouterView />
    </main>
  </div>
</template>
