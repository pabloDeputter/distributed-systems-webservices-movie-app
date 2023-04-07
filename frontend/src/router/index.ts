import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import("../views/HomeView.vue"),
    },
    {
      path: "/account",
      name: "Account",
      component: () => import("../views/AccountView.vue"),
    },
    {
      path: "/movie/:id",
      name: "Movie",
      component: () => import("../views/MovieView.vue"),
    },
    {
      path: "/popular-movies",
      name: "popularMovies",
      component: () => import("../views/PopularMoviesView.vue"),
    },
    {
      path: "/similar-movies",
      name: "similarMovies",
      component: () => import("../views/SimilarMoviesView.vue"),
    },
    {
      path: "/score-movies",
      name: "scoreMovies",
      component: () => import("../views/ScoreMoviesView.vue"),
    },
  ],
});

export default router;
