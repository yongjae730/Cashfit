import axios from "axios";
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import router from "@/router";

export const useAccount = defineStore(
  "accounts",
  () => {
    const API_URL = "http://127.0.0.1:8000";
    const token = ref(null);
    const showLoginMoal = ref(false);
    const isLogin = computed(() => token.value !== null);
    const redirectPath = ref(null);
    const login = async (payload) => {
      try {
        const { username, password } = payload;
        const response = await axios.post(`${API_URL}/accounts/login/`, { username, password });
        token.value = response.data.key;
        const redirectTo = redirectPath.value || { name: "Main" };
        redirectPath.value = null;
        router.push(redirectTo);
      } catch (err) {
        console.error("Login failed:", err);
      }
    };

    const signUp = async (payload) => {
      try {
        const { username, password1, password2, nickname, age, capital, sido, sigungus } = payload;
        await axios.post(`${API_URL}/accounts/signup/`, { username, password1, password2, nickname, age, capital, sido, sigungus });
        await login({ username, password: password1 });
      } catch (err) {
        console.error("Signup failed:", err.response?.data || err);
      }
    };

    return { API_URL, token, isLogin, login, signUp, showLoginMoal, redirectPath };
  },
  { persist: true }
);
