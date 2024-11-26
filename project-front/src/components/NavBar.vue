<template>
  <v-app-bar :class="{ scrolled: isScrolled }" app flat>
    <v-container>
      <v-row justify="space-between" align="center">
        <!-- 로고 영역 -->
        <v-col class="d-flex align-center">
          <router-link to="/"><v-img :src="`/bank_images/logo_no_bg.png`" width="100px"></v-img></router-link>
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
            <v-btn outlined class="mr-2" @click="showLoginModal = true">로그인</v-btn>
            <router-link to="/sign_up">
              <v-btn color="black" dark>회원가입</v-btn>
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
  color: inherit;
}

/* v-app-bar 전역 스타일 재정의 */
:deep(.v-app-bar) {
  background-color: #7686b3 !important; /* 캐러셀 배경색과 동일한 색상 */
  transition: all 0.3s ease-in-out;
}

:deep(.v-toolbar) {
  background-color: #7686b3 !important;
}

/* 스크롤되지 않은 상태 - 캐러셀 배경색 */
.v-app-bar:not(.scrolled) {
  background-color: #7686b3 !important;
  box-shadow: none !important;
}

.v-app-bar:not(.scrolled) :deep(.v-toolbar__content) {
  background-color: #7686b3 !important;
}

/* 스크롤되지 않은 상태의 텍스트/버튼 색상 */
.v-app-bar:not(.scrolled) .v-btn {
  color: white !important; /* 텍스트 색상을 흰색으로 변경 */
}

.v-app-bar:not(.scrolled) a {
  color: white !important;
}

/* 스크롤된 상태 - 흰색 배경 */
.v-app-bar.scrolled {
  background-color: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
}

.v-app-bar.scrolled :deep(.v-toolbar__content) {
  background-color: rgba(255, 255, 255, 0.95) !important;
}

/* 스크롤된 상태의 텍스트/버튼 색상 */
.v-app-bar.scrolled .v-btn {
  color: black !important;
}

.v-app-bar.scrolled a {
  color: black !important;
}

/* 나머지 스타일 */
.dropdown-btn {
  background-color: transparent;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  padding: 6px 12px;
  text-transform: none;
  transition: all 0.3s ease;
}

.dropdown-menu {
  background-color: #ffffff;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-width: 150px;
  overflow: hidden;
}

.v-btn {
  text-transform: none !important;
  letter-spacing: 0;
  font-weight: 500;
  transition: all 0.3s ease;
}

.v-btn:hover {
  opacity: 0.8;
  background-color: rgba(255, 255, 255, 0.1); /* hover 색상 변경 */
}
</style>
