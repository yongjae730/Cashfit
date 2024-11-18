<template>
  <v-main>
    <v-container>
      <MainPageCarousel :slides="carouselSlides" />
      <MainPageFinProduct />
      <MapTest />
    </v-container>
  </v-main>
</template>

<script setup>
import MainPageCarousel from "@/components/MainPageCarousel.vue";
import MainPageFinProduct from "@/components/MainPageFinProduct.vue";
import MapTest from "@/components/MapTest.vue";
import { ref, computed, onMounted } from "vue";

// 캐러셀 데이터
const carouselSlides = ref([]);

onMounted(() => {
  carouselSlides.value = [
    {
      image: "https://via.placeholder.com/1200x400",
      title: "금융 상품 추천",
      subtitle: "당신을 위한 맞춤 금융 상품",
    },
    {
      image: "https://via.placeholder.com/1200x400",
      title: "실시간 주식 정보",
      subtitle: "빠르고 정확한 시장 동향",
    },
    {
      image: "https://via.placeholder.com/1200x400",
      title: "암호화폐 시세",
      subtitle: "글로벌 암호화폐 동향",
    },
  ];
});
</script>

<style scoped></style>
