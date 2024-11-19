<template>
  <v-app>
    <NavBar />
    <RouterView />
    <LoginModal :is-open="showLoginModal" @update:is-open="updateLoginModal" />
    <Footer />
  </v-app>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
import Footer from "./components/Footer.vue";
import { computed, onMounted } from "vue";
import axios from "axios";
import { useAccount } from "./stores/accounts";
import LoginModal from "./components/LoginModal.vue";

const accountStore = useAccount();
const showLoginModal = computed(() => accountStore.showLoginMoal);

const updateLoginModal = (isOpen) => {
  accountStore.showLoginMoal = isOpen;
};
// onMounted(() => {
//   axios.get(`http://127.0.0.1:8000/api/financials/save-financial-products/`);
// });
</script>
<style scoped></style>
