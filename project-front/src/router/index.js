import { createRouter, createWebHistory } from "vue-router";
import MainView from "@/views/MainView.vue";
import SignUpView from "@/views/SignUpView.vue";
import FinView from "@/views/FinView.vue";
import StockView from "@/views/StockView.vue";
import CryptoView from "@/views/CryptoView.vue";
import FinDetailView from "@/views/FinDetailView.vue";

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
      path: "/stock",
      name: "Stock",
      component: StockView,
    },
    {
      path: "/crypto",
      name: "Crypto",
      component: CryptoView,
    },
    {
      path: "/fin/:fin_prdt_cd",
      name: "finDetail",
      component: FinDetailView,
    },
  ],
});

export default router;
