<template>
  <v-container class="py-8">
    <!-- 상단 프로필 정보 -->
    <v-card class="mb-6" elevation="2" rounded="lg">
      <v-card-title class="d-flex justify-space-between align-center">
        <div>
          <h1 class="text-h4 font-weight-bold">프로필 페이지</h1>
          <p class="text-subtitle-2 text-grey-darken-1">사용자 정보를 확인하고 관리하세요</p>
        </div>
        <v-btn color="primary" outlined class="font-weight-bold" @click="editProfile">회원 정보 수정</v-btn>
      </v-card-title>
    </v-card>

    <!-- 콘텐츠 섹션 -->
    <v-row dense>
      <!-- 마이 페이지 -->
      <v-col cols="12" md="4">
        <v-card elevation="2" outlined rounded="lg" class="h-100">
          <v-card-title class="font-weight-bold text-h6">마이 페이지</v-card-title>
          <v-card-text>
            <div>회원 정보를 확인하거나 변경하세요.</div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="secondary" block rounded @click="editProfile">수정</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- 내 금융 상품 -->
      <v-col cols="12" md="8">
        <v-card elevation="2" outlined rounded="lg" class="h-100">
          <v-tabs background-color="primary" dark>
            <v-tab>내 예금</v-tab>
            <v-tab>내 적금</v-tab>

            <v-tab-item>
              <v-card-text>
                <div v-if="deposits.length">
                  <v-list dense>
                    <v-list-item v-for="(deposit, index) in deposits" :key="index" class="py-2">
                      <v-list-item-content>
                        <v-list-item-title>{{ deposit.name }}</v-list-item-title>
                        <v-list-item-subtitle>{{ deposit.details }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </div>
                <div v-else>저장된 예금 상품이 없습니다.</div>
              </v-card-text>
            </v-tab-item>

            <v-tab-item>
              <v-card-text>
                <div v-if="savings.length">
                  <v-list dense>
                    <v-list-item v-for="(saving, index) in savings" :key="index" class="py-2">
                      <v-list-item-content>
                        <v-list-item-title>{{ saving.name }}</v-list-item-title>
                        <v-list-item-subtitle>{{ saving.details }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </div>
                <div v-else>저장된 적금 상품이 없습니다.</div>
              </v-card-text>
            </v-tab-item>
          </v-tabs>
        </v-card>
      </v-col>
    </v-row>

    <!-- 내가 쓴 글 -->
    <v-card class="my-6" elevation="2" outlined rounded="lg">
      <v-card-title class="font-weight-bold text-h6">내가 쓴 글</v-card-title>
      <v-card-text>
        <div v-if="myPosts.length">
          <v-list dense>
            <v-list-item v-for="(post, index) in myPosts" :key="index">
              <v-list-item-content>
                <v-list-item-title>{{ post.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ post.date }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </div>
        <div v-else>작성한 글이 없습니다.</div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";

// 샘플 데이터
const deposits = ref([
  { name: "예금 상품 A", details: "이율 2.5%, 기간 1년" },
  { name: "예금 상품 B", details: "이율 3.0%, 기간 2년" },
]);

const savings = ref([
  { name: "적금 상품 A", details: "월 납입액 10만 원, 기간 3년" },
  { name: "적금 상품 B", details: "월 납입액 20만 원, 기간 5년" },
]);

const myPosts = ref([
  { title: "저축 팁 공유", date: "2024-11-19" },
  { title: "예금과 적금의 차이", date: "2024-11-18" },
]);

const editProfile = () => {
  alert("회원 정보 수정 모달을 띄웁니다.");
};
</script>

<style scoped>
.v-card {
  border-radius: 16px;
}
</style>
