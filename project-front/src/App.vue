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
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css");
* {
  background-color: #eef7fb;
  font-family: "Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
  font-weight: 400; /* 기본 본문 폰트 웨이트 */
  letter-spacing: -0.4px;
  line-height: 1.6;
}

/* 제목 스타일 */
h1 {
  font-weight: 600; /* 타이틀 진하게 */
  font-size: 24px;
}

h2 {
  font-weight: 500; /* 소제목 중간 굵기 */
  font-size: 20px;
}

p,
span {
  font-weight: 400; /* 본문 기본 굵기 */
}

small,
.caption {
  font-weight: 300; /* 캡션 가볍게 */
  font-size: 12px;
}

/* 반응형 대응 */
@media (max-width: 600px) {
  h1 {
    font-size: 20px;
  }
  h2 {
    font-size: 18px;
  }
  small,
  .caption {
    font-size: 10px;
  }
}
</style>

<!-- /* 
<script setup>
// 폰트 weight 사용 예시
const fontWeights = {
  title: 600,       // 제목
  subtitle: 500,    // 소제목
  body: 400,        // 본문
  caption: 300      // 캡션
}
</script> */ -->
