import NotFoundView from "@/views/NotFoundView.vue";
import { createRouter, createWebHistory } from "vue-router";
import NewsView from "@/views/NewsView.vue";
import NewsDetailView from "@/views/NewsDetailView.vue";
import DashBoardView from "@/views/DashBoardView.vue";
import RegisterView from "@/views/RegisterView.vue";
import LoginView from "@/views/LoginView.vue";
import LandingView from "@/views/LandingView.vue";
import SettingsView from "@/views/SettingsView.vue";


const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: "/",
      name: "landing",
      component: LandingView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/news",
      name: "News",
      component: NewsView,
      meta: { chatbot: true },
    },
    {
      path: "/news/:id",
      name: "newsDetail",
      component: NewsDetailView,
      props: true,
      meta: { requiresAuth: true, chatbot: true },
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: DashBoardView,
      meta: { requiresAuth: true },
    },
    {
      path: "/settings",
      name: "settings",
      component: SettingsView,
      meta: { requiresAuth: true },
    },
    {
      path: "/:pathMatch(.*)*",
      component: NotFoundView,
    },
  ],
});

export default router;

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access');

  if (to.meta.requiresAuth && !isAuthenticated) {
    alert("로그인이 필요합니다.");
    next('/login');
  } else {
    next();
  }
});
