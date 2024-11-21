<template>
  <v-main>
    <MainPageCarousel v-if="carouselSlides.length > 0" :slides="carouselSlides" />
    <MiddleNav />
    <v-container>
      <MainProductList />
      <MainPageBank />
    </v-container>
  </v-main>
</template>

<script setup>
import MainPageCarousel from "@/components/MainPageCarousel.vue";
import MainProductList from "@/components/MainProductList.vue";
import MainPageBank from "@/components/MainPageBank.vue";
import { ref, onMounted } from "vue";
import MiddleNav from "@/components/MiddleNav.vue";

// 캐러셀 데이터
const carouselSlides = ref([]);

const fetchCarouselSlides = async () => {
  // 데이터를 가져오는 비동기 함수
  return [
    {
      image: "https://via.placeholder.com/1200x400",
      title: "금융 상품 추천",
      subtitle: "당신을 위한 맞춤 금융 상품",
    },
    {
      image: "https://via.placeholder.com/1200x400",
      title: "내 주변 은행 머임?",
      subtitle: "찾기 귀찮쓰",
    },
    {
      image: "https://via.placeholder.com/1200x400",
      title: "AI에게 물어본 내 투자 방향",
      subtitle: "지려따...",
    },
    {
      image: "https://via.placeholder.com/1200x400",
      title: "예적금 토론 ㄱㄱ",
      subtitle: "ㅇㅅㅇ",
    },
  ];
};

onMounted(async () => {
  // 데이터를 비동기적으로 가져옴
  carouselSlides.value = await fetchCarouselSlides();
});
</script>

<style scoped></style>
