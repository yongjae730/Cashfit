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
            <v-btn text>커뮤니티</v-btn>
          </router-link>
          <router-link :to="{ name: 'crypto' }">
            <v-btn text>비트코인</v-btn>
          </router-link>
        </v-col>

        <!-- 로그인/회원가입 버튼 -->
        <v-col class="d-flex align-center" cols="auto">
          <template v-if="isLogin">
            <v-menu offset-y>
              <template #activator="{ props }">
                <v-btn text v-bind="props">{{ username }}</v-btn>
              </template>
              <v-list-item>
                <!-- <RouterLink :to="{ name: 'profile', params: { id: user } }">내 프로필</RouterLink> -->
              </v-list-item>
              <v-list-item @click="logout">로그아웃</v-list-item>
            </v-menu>
          </template>
          <template v-else>
            <v-btn outlined class="mr-2" @click="showLoginModal = true">Sign in</v-btn>
            <v-btn color="black" dark><router-link to="/sign_up">Register</router-link></v-btn>
          </template>
        </v-col>
      </v-row>
    </v-container>

    <login-modal :is-open="showLoginModal" @update:is-open="showLoginModal = $event" />
  </v-app-bar>
</template>

<script setup>
import { computed, ref } from "vue";
import LoginModal from "./LoginModal.vue";
import { useAccount } from "@/stores/accounts";

const showLoginModal = ref(false);
const user = ref(null);
const store = useAccount();
const isLogin = computed(() => store.isLogin);
const username = computed(() => store.username || "User");
console.log(store.user);
user.value = store.user;
const logout = () => {
  store.token = null;
  store.username = null;
};
</script>

<style scoped>
a {
  text-decoration: none;
  color: black;
}
</style>
