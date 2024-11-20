<template>
  <v-container style="margin-top: 64px">
    <!-- 상단 프로필 정보 -->
    <v-card class="mb-6 profile-card">
      <v-card-title class="d-flex justify-space-between align-center">
        <div>
          <h1 class="text-h4 font-weight-bold">프로필 페이지</h1>
          <p class="text-subtitle-2 text-grey-darken-1">사용자 정보를 확인하고 관리하세요</p>
        </div>
        <v-btn color="primary" rounded class="font-weight-bold px-4" @click="editProfile">회원 정보 수정</v-btn>
      </v-card-title>
    </v-card>

    <!-- 콘텐츠 섹션 -->
    <v-row dense>
      <!-- 마이 페이지 -->
      <v-col cols="12" md="4">
        <v-card class="info-card">
          <v-card-title class="font-weight-bold text-h6">마이 페이지</v-card-title>
          <v-card-text>
            <div class="info-text">회원 정보를 확인하거나 변경하세요.</div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="secondary" block rounded @click="editProfile">정보 수정</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12">
        <!-- 예금 캐러셀 -->
        <v-card class="info-card mb-6">
          <v-card-title class="font-weight-bold text-h6">내 예금</v-card-title>
          <v-card-text>
            <div v-if="deposits.length">
              <v-carousel class="carousel-container" hide-delimiters show-arrows height="300px">
                <v-carousel-item v-for="(deposit, index) in deposits" :key="index">
                  <v-card outlined class="carousel-card">
                    <!-- 좋아요 취소 버튼 -->
                    <v-btn icon color="red" class="like-button" @click="unlikeProduct(deposit.id, 0)">
                      <v-icon>mdi-heart</v-icon>
                    </v-btn>
                    <!-- 은행 로고 -->
                    <v-card-title class="bank-info d-flex align-center">
                      <v-avatar size="36" class="mr-3">
                        <v-img :src="`/bank_images/${deposit.kor_co_nm}.jpg`" max-width="120px" class="mr-6 rounded-lg" cover alt="상품 이미지"></v-img>
                      </v-avatar>
                      <span class="bank-name">{{ deposit.kor_co_nm }}</span>
                    </v-card-title>
                    <!-- 상품 정보 -->
                    <v-card-title class="product-title">
                      {{ deposit.fin_prdt_nm }}
                    </v-card-title>
                    <v-card-text class="product-details">
                      <ul class="details-list">
                        <li>{{ deposit.etc_note }}</li>
                      </ul>
                    </v-card-text>
                  </v-card>
                </v-carousel-item>
              </v-carousel>
            </div>
            <div v-else class="empty-state">좋아요한 예금 상품이 없습니다.</div>
          </v-card-text>
        </v-card>

        <!-- 적금 캐러셀 -->
        <v-card class="info-card">
          <v-card-title class="font-weight-bold text-h6">내 적금</v-card-title>
          <v-card-text>
            <div v-if="savings.length">
              <v-carousel class="carousel-container" hide-delimiters show-arrows height="300px">
                <v-carousel-item v-for="(saving, index) in savings" :key="index">
                  <v-card outlined class="carousel-card">
                    <!-- 좋아요 취소 버튼 -->
                    <v-btn icon color="red" class="like-button" @click="unlikeProduct(saving.id, 1)">
                      <v-icon>mdi-heart</v-icon>
                    </v-btn>
                    <!-- 은행 로고 -->
                    <v-card-title class="bank-info d-flex align-center">
                      <v-avatar size="36" class="mr-3">
                        <v-img :src="`/bank_images/${saving.kor_co_nm}.jpg`" max-width="120px" class="mr-6 rounded-lg" cover alt="상품 이미지"></v-img>
                      </v-avatar>
                      <span class="bank-name">{{ saving.kor_co_nm }}</span>
                    </v-card-title>
                    <!-- 상품 정보 -->
                    <v-card-title class="product-title">
                      {{ saving.fin_prdt_nm }}
                    </v-card-title>
                    <v-card-text class="product-details">
                      <ul class="details-list">
                        <li>{{ saving.etc_note }}</li>
                      </ul>
                    </v-card-text>
                  </v-card>
                </v-carousel-item>
              </v-carousel>
            </div>
            <div v-else class="empty-state">좋아요한 적금 상품이 없습니다.</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 내가 쓴 글 -->
    <v-card class="my-6 info-card">
      <v-card-title class="font-weight-bold text-h6">내가 쓴 글</v-card-title>
      <v-card-text>
        <div v-if="articles.length">
          <v-list dense>
            <v-list-item v-for="(post, index) in articles" :key="index" class="post-item">
              <v-list-item-content>
                <RouterLink :to="{ name: 'articleDetail', params: { id: post.id } }">
                  <v-list-item-title class="post-title">{{ post.title }}</v-list-item-title>
                </RouterLink>
                <v-list-item-subtitle class="post-date">{{ post.create_at }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </div>
        <div v-else class="empty-state">작성한 글이 없습니다.</div>
      </v-card-text>
    </v-card>

    <!-- 내가 쓴 댓글 -->
    <v-card class="my-6 info-card">
      <v-card-title class="font-weight-bold text-h6">내가 쓴 댓글</v-card-title>
      <v-card-text>
        <div v-if="comments.length">
          <v-list dense>
            <v-list-item v-for="(comment, index) in comments" :key="index" class="post-item">
              <v-list-item-content>
                <v-list-item-title class="post-title">{{ comment.content }}</v-list-item-title>
                <v-list-item-subtitle class="post-date">{{ comment.create_at }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </div>
        <div v-else class="empty-state">작성한 댓글이 없습니다.</div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { useAccount } from "@/stores/accounts";
import { computed, watchEffect } from "vue";
import axios from "axios";

const accountStore = useAccount();
const isLogin = computed(() => accountStore.isLogin);
const API_URL = "http://127.0.0.1:8000"; // API URL 설정

const { articles, comments, user_info } = accountStore.user;
watchEffect(() => {
  if (isLogin.value) {
    accountStore.getProfile(); // 로그인 시 프로필 정보를 가져옵니다.
    articles, comments;
  }
});

console.log(articles, comments);

// 좋아요한 상품 데이터
const likedProducts = computed(() => accountStore.user?.liked_products || []);

// 예금과 적금으로 필터링
const deposits = computed(() => likedProducts.value.filter((product) => product.product_type === 0));

const savings = computed(() => likedProducts.value.filter((product) => product.product_type === 1));

// 좋아요 취소 메서드
const unlikeProduct = async (productId, productType) => {
  try {
    const headers = {
      Authorization: `Token ${accountStore.token}`,
    };

    // 좋아요 취소 요청
    await axios.delete(`${API_URL}/api/financials/products/${productId}/like/`, { headers });

    // 배열에서 제거
    if (productType === 0) {
      accountStore.user.liked_products = likedProducts.value.filter((product) => product.id !== productId);
    } else if (productType === 1) {
      accountStore.user.liked_products = likedProducts.value.filter((product) => product.id !== productId);
    }
  } catch (error) {
    console.error("좋아요 취소 실패:", error);
  }
};
</script>

<style scoped>
/* 프로필 카드 */
.info-card {
  border-radius: 16px;
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.12);
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
  padding: 16px;
  margin-bottom: 16px;
}

/* 캐러셀 컨테이너 */
.carousel-container {
  max-width: 600px; /* 캐러셀 크기를 카드 크기에 맞춤 */
  margin: 0 auto; /* 가운데 정렬 */
}

/* 캐러셀 카드 */
.carousel-card {
  height: 260px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 16px;
  text-align: left;
  border-radius: 16px;
  background-color: #f9f9f9;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

/* 은행 정보 */
.bank-info {
  margin-bottom: 12px;
}

.bank-name {
  font-size: 1rem;
  font-weight: bold;
  color: #3f51b5;
}

/* 상품 정보 */
.product-title {
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 8px;
  color: #333;
}

.product-details {
  font-size: 0.9rem;
  color: #666;
}

.details-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.details-list li {
  margin-bottom: 4px;
  line-height: 1.5;
}

/* 빈 상태 텍스트 */
.empty-state {
  text-align: center;
  color: #9e9e9e;
  font-style: italic;
  margin: 16px 0;
}
/* 리스트 아이템 스타일 */
.product-item,
.post-item {
  transition: background-color 0.2s ease;
}

.product-item:hover,
.post-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.product-details,
.post-date {
  font-size: 0.9rem;
  color: #6c757d;
}

.info-text {
  font-size: 0.95rem;
  color: #495057;
}
</style>
