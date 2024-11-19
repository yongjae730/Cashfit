import { createRouter, createWebHistory } from "vue-router";
import MainView from "@/views/MainView.vue";
import SignUpView from "@/views/SignUpView.vue";
import FinView from "@/views/FinView.vue";
import StockView from "@/views/CommunityView.vue";
import CryptoView from "@/views/CryptoView.vue";
import CommunityView from "@/views/CommunityView.vue";
import CreateArticleView from "@/views/CreateArticleView.vue";
import { useAccount } from "@/stores/accounts";
import CommunityDetailView from "@/views/CommunityDetailView.vue";
import ProductDetailView from "@/views/ProductDetailView.vue";
import ProfileView from "@/views/ProfileView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Main",
      component: MainView,
    },
    {
      path: "/fin",
      name: "fin",
      component: FinView,
    },
    {
      path: "/stock",
      name: "stock",
      component: StockView,
    },
    {
      path: "/crypto",
      name: "crypto",
      component: CryptoView,
    },
    {
      path: "/sign_up",
      name: "SignUp",
      component: SignUpView,
    },
    {
      path: "/fin",
      name: "Fin",
      component: FinView,
    },
    {
      path: "/community",
      name: "community",
      component: CommunityView,
    },
    {
      path: "/crypto",
      name: "Crypto",
      component: CryptoView,
    },

    {
      path: "/community/create_article",
      name: "createArticle",
      component: CreateArticleView,
      meta: { isLogin: true },
    },
    {
      path: "/community/:id",
      name: "articleDetail",
      component: CommunityDetailView,
    },
    {
      path: "/product/:id",
      name: "productDetail",
      component: ProductDetailView,
    },
    {
      path: "/profile/:id",
      name: "profile",
      component: ProfileView,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const accountStore = useAccount();

  if (to.meta.isLogin && !accountStore.isLogin) {
    accountStore.showLoginMoal = true;
    accountStore.redirectPath = to.fullPath;
    return next(false);
  }
  next();
});

export default router;
