import axios from "axios";
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import router from "@/router";

export const useAccount = defineStore(
  "accounts",
  () => {
    const API_URL = "http://127.0.0.1:8000";
    const token = ref(null);
    const user = ref(null);
    const redirectPath = ref(null);

    const isLogin = computed(() => token.value !== null);

    const login = async (payload) => {
      try {
        const { username, password } = payload;
        const response = await axios.post(`${API_URL}/accounts/login/`, { username, password });
        token.value = response.data.key;
        user.value = response.data.user;

        const redirectTo = redirectPath.value || { name: "Main" };
        redirectPath.value = null;
        router.push(redirectTo);
      } catch (err) {
        console.error("Login failed:", err.response?.data || err.message);
        throw err;
      }
    };

    const signUp = async (payload) => {
      try {
        const { username, password1, password2, nickname, age, capital, sido, sigungus } = payload;
        await axios.post(`${API_URL}/accounts/signup/`, { username, password1, password2, nickname, age, capital, sido, sigungus });
        await login({ username, password: password1 });
      } catch (err) {
        console.error("Signup failed:", err.response?.data || err.message);
        throw err;
      }
    };

    const getProfile = async () => {
      if (!token.value) return;

      try {
        const response = await axios.get(`${API_URL}/accounts/user_profile/`, {
          headers: { Authorization: `Token ${token.value}` },
        });
        user.value = response.data;
      } catch (error) {
        console.error("Failed to fetch profile:", error.response?.data || error.message);
      }
    };

    return { API_URL, token, user, isLogin, login, signUp, getProfile, redirectPath };
  },
  { persist: true }
);
