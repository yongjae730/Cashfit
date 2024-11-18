
<template>
  <v-app>
    <NavBar />
    <keep-alive>
      <RouterView />
    </keep-alive>
    <Footer />
  </v-app>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
import Footer from "./components/Footer.vue";
import { onMounted } from "vue";
import axios from "axios";

  onMounted(() => {
    axios.get(`http://127.0.0.1:8000/api/financials/save-financial-products/`)
  })
 </script>
<style scoped>
</style>
