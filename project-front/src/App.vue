<script setup>
import { RouterLink, RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
import Footer from "./components/Footer.vue";
</script>

<template>
  <v-app>
    <NavBar />
    <RouterView />
    <Footer />
  </v-app>
</template>

<style scoped></style>
