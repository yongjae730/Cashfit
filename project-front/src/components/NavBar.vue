<template>
  <v-app-bar :class="{ scrolled: isScrolled }" app flat>
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
          <router-link :to="{ name: 'exchange' }">
            <v-btn text>환율조회</v-btn>
          </router-link>
          <router-link :to="{ name: 'crypto' }">
            <v-btn text>암호화폐</v-btn>
          </router-link>
        </v-col>

        <!-- 로그인/회원가입 버튼 -->
        <v-col class="d-flex align-center" cols="auto">
          <template v-if="isLogin">
            <v-menu offset-y>
              <template #activator="{ props }">
                <v-btn text class="dropdown-ntn" v-bind="props">{{ username }}</v-btn>
              </template>
              <v-list class="dropdown-menu">
                <v-list-item @click="logout">로그아웃</v-list-item>
                <RouterLink :to="{ name: 'profile', params: { nickname: user_info.nickname } }"><v-list-item>마이 페이지</v-list-item></RouterLink>
              </v-list>
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
import { computed, onMounted, onUnmounted, ref, watchEffect } from "vue";
import LoginModal from "./LoginModal.vue";
import { useAccount } from "@/stores/accounts";
import router from "@/router";

const showLoginModal = ref(false);
const store = useAccount();
const isLogin = computed(() => store.isLogin);
const user_info = computed(() => store.user?.user_info || {}); // store.user가 null이어도 안전하게 처리
const username = computed(() => user_info.value.nickname || "User");

const isScrolled = ref(false);

// 스크롤 이벤트 핸들러
const handleScroll = () => {
  isScrolled.value = window.scrollY > 0;
};

// 스크롤 이벤트 등록 및 해제
onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});

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
.v-app-bar {
  background-color: transparent;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

/* 스크롤 상태: 흰색 */
.v-app-bar.scrolled {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 드롭다운 스타일 (기존 유지) */
.dropdown-btn {
  background-color: #f5f5f5;
  color: #222;
  font-weight: bold;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 6px 12px;
  text-transform: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.dropdown-btn:hover {
  background-color: #e0e0e0;
  color: #000;
}

.dropdown-menu {
  background-color: #ffffff;
  border-radius: 12px;
  border: 1px solid #ddd;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  min-width: 150px;
}
</style>
