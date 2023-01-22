import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/StandardLogin.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("../views/profile/RegisterView.vue"),
    },
    {
      path: "/activation/:uid/:token",
      name: "activation",
      component: () => import("../views/profile/ActivationView.vue"),
    },
    {
      path: "/activation/",
      name: "resend_activation",
      component: () => import("../views/profile/ActivationView.vue"),
    },
    {
      path: "/profile",
      name: "profile",
      component: () => import("../views/profile/MyProfile.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/myorgas",
      name: "myorgas",
      component: () => import("../views/profile/MyOrgas.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/myposts",
      name: "myposts",
      component: () => import("../views/profile/MyPosts.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/search",
      name: "search",
      component: () => import("../views/SearchPost.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/post/:postid",
      name: "showpost",
      component: () => import("../views/ShowPost.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/editpost/:postid",
      name: "editpost",
      component: () => import("../views/EditPost.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/editorga/:orgaid",
      name: "editorga",
      component: () => import("../views/orgas/EditOrga.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/orga/:orgaid",
      name: "showorga",
      component: () => import("../views/orgas/ShowOrga.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
  ],
});
router.beforeEach(async (to) => {
  const store = useAuthStore();
  if (!store.isAuthenticated) {
    await store.checkAuth();
  }
  if (to.meta.requiresAuth && !store.isAuthenticated) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    return {
      path: "/login",
      // save the location we were at to come back later
      query: { redirect: to.fullPath },
    };
  }
});

export default router;
