<template>
  <v-app-bar app flat color="#f8f9fa">
    <v-container>
      <v-row justify="space-between" align="center">
        <!-- 로고 영역 -->
        <v-col class="d-flex align-center">
          <router-link to="/"><v-icon>mdi-github</v-icon></router-link>
        </v-col>

        <!-- 메뉴 -->
        <v-col class="d-flex align-center" cols="auto">
          <router-link :to="{ name: 'fin' }">
            <v-btn text>금융상품</v-btn>
          </router-link>
          <router-link :to="{ name: 'stock' }">
            <v-btn text>주식</v-btn>
          </router-link>
          <router-link :to="{ name: 'crypto' }">
            <v-btn text>비트코인</v-btn>
          </router-link>
        </v-col>

        <!-- 로그인/회원가입 버튼 -->
        <v-col class="d-flex align-center" cols="auto">
          <v-btn outlined class="mr-2" @click="showLoginModal = true">Sign in</v-btn>
          <v-btn color="black" dark><router-link to="/sign_up">Register</router-link></v-btn>
        </v-col>
      </v-row>
    </v-container>

    <login-modal :is-open="showLoginModal" @update:is-open="showLoginModal = $event" />
  </v-app-bar>
</template>

<script setup>
import { ref } from "vue";
import LoginModal from "./LoginModal.vue";

const showLoginModal = ref(false);
</script>

<style scoped>
a {
  text-decoration: none;
  color: black;
}
</style>
