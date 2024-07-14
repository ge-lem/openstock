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
      path: "/contact",
      name: "contact",
      component: () => import("../views/ContactPage.vue"),
    },
    {
      path: "/credits",
      name: "credits",
      component: () => import("../views/CreditsPage.vue"),
    },
    {
      path: "/datapolicy",
      name: "datapolicy",
      component: () => import("../views/DataPolicy.vue"),
    },
    {
      path: "/legalnotice",
      name: "legalnotice",
      component: () => import("../views/LegalNotice.vue"),
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
      path: "/password/reset/",
      name: "reset_password",
      component: () => import("../views/profile/ResetPassword.vue"),
      meta: { requiresNotAuth: true },
    },
    {
      path: "/password/reset/confirm/:uid/:token",
      name: "reset_password_confirm",
      component: () => import("../views/profile/ResetPasswordConfirm.vue"),
      meta: { requiresNotAuth: true },
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
      path: "/orgas",
      name: "listorgas",
      component: () => import("../views/orgas/ListOrgas.vue"),
      meta: { requiresAuth: true },
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
  } else if (to.meta.requiresNotAuth && store.isAuthenticated) {
    return {
      path: "/",
    };
  }
});

export default router;
