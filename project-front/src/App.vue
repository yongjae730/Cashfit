<template>
  <v-app>
    <NavBar />
    <RouterView />
    <LoginModal :is-open="showLoginModal" @update:is-open="updateLoginModal" />
    <Footer />
    <ChatbotWidget />
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
import ChatbotWidget from "./components/ChatbotWidget.vue";

const accountStore = useAccount();
const showLoginModal = computed(() => accountStore.showLoginMoal);

const updateLoginModal = (isOpen) => {
  accountStore.showLoginMoal = isOpen;
};
// onMounted(() => {
//   axios.get(`http://127.0.0.1:8000/api/financials/save-financial-products/`);
// });
</script>
<style scoped>
* {
  background: #f9f9f9;
}
html,
body {
  font-family: "Noto Sans", sans-serif;
}
.display-large {
  font-size: 3.5rem;
  font-weight: bold;
  line-height: 1.2;
  color: var(--v-primary-base);
}

.headline-medium {
  font-size: 2rem;
  font-weight: 600;
  line-height: 1.5;
}

.subtitle-medium {
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--v-secondary-base);
}
</style>
