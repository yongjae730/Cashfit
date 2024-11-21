<template>
  <v-app-bar app flat color="#ffffff">
    <v-container>
      <v-row justify="space-between" align="center">
        <!-- 로고 영역 -->
        <v-col class="d-flex align-center">
          <router-link to="/"><v-img :src="`/bank_images/로고.png`" width="100px"></v-img></router-link>
        </v-col>

        <!-- 메뉴 -->
        <v-col class="d-flex align-center" cols="auto">
          <router-link :to="{ name: 'fin' }">
            <v-btn text>금융상품</v-btn>
          </router-link>
          <router-link :to="{ name: 'stock' }">
            <v-btn text>커뮤니티</v-btn>
          </router-link>
          <router-link :to="{ name: 'crypto' }">
            <v-btn text>비트코인</v-btn>
          </router-link>
          <router-link :to="{ name: 'exchange' }">
            <v-btn text>Exchange</v-btn>
          </router-link>
        </v-col>

        <!-- 로그인/회원가입 버튼 -->
        <v-col class="d-flex align-center" cols="auto">
          <template v-if="isLogin">
            <v-menu offset-y>
              <template #activator="{ props }">
                <v-btn text v-bind="props">{{ username }}</v-btn>
              </template>
              <v-list-item @click="logout">로그아웃</v-list-item>
              <RouterLink :to="{ name: 'profile', params: { nickname: user_info.nickname } }"><v-list-item>마이 페이지</v-list-item></RouterLink>
            </v-menu>
          </template>
          <template v-else>
            <v-btn outlined class="mr-2" @click="showLoginModal = true">Sign in</v-btn>
            <router-link to="/sign_up">
              <v-btn color="black" dark>Register</v-btn>
            </router-link>
          </template>
        </v-col>
      </v-row>
    </v-container>

    <login-modal :is-open="showLoginModal" @update:is-open="showLoginModal = $event" />
  </v-app-bar>
</template>

<script setup>
import { computed, ref, watchEffect } from "vue";
import LoginModal from "./LoginModal.vue";
import { useAccount } from "@/stores/accounts";
import router from "@/router";

const showLoginModal = ref(false);
const store = useAccount();
const isLogin = computed(() => store.isLogin);
const user_info = computed(() => store.user?.user_info || {}); // store.user가 null이어도 안전하게 처리
const username = computed(() => user_info.value.nickname || "User");

const logout = () => {
  store.token = null;
  store.user = null;
  router.push({ name: "Main" });
};

// 로그인 시 getProfile 호출해서 프로필 정보를 업데이트
watchEffect(() => {
  if (isLogin.value) {
    store.getProfile(); // 로그인 시 프로필 정보를 가져옵니다.
  }
});
</script>

<style scoped>
a {
  text-decoration: none;
  color: black;
}
</style>
