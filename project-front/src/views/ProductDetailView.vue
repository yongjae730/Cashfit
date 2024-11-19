<template>
  <v-container style="margin-top: 64px">
    <!-- 상품 제목 섹션 -->
    <v-card class="mb-6" elevation="2">
      <v-card-title class="d-flex align-center">
        <!-- <v-avatar size="150"> -->
        <v-img :src="`/bank_images/${product.kor_co_nm}.jpg`" max-width="150px" alt="상품 이미지" class="mr-4"></v-img>
        <!-- </v-avatar> -->
        <div>
          <div class="text-h5 font-weight-bold">{{ product.fin_prdt_nm }}</div>
          <div class="text-subtitle-2 text-grey-darken-2">{{ product.kor_co_nm }}</div>
        </div>
      </v-card-title>
    </v-card>

    <!-- 상품 정보 섹션 -->
    <v-row>
      <v-col cols="12" sm="6" md="4" v-for="(item, index) in productDetails" :key="index">
        <v-card outlined class="py-4 px-6 text-center elevation-1">
          <v-icon size="36" class="mb-2" color="primary">mdi-information-outline</v-icon>
          <div class="text-h6 font-weight-bold">{{ item.label }}</div>
          <div class="text-body-2 text-grey-darken-1">{{ item.value }}</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- 상품 설명 -->
    <v-card class="my-6" outlined>
      <v-card-title class="text-h6 font-weight-bold">상품 설명</v-card-title>
      <v-card-text class="text-body-2">
        {{ product.etc_note }}
      </v-card-text>
    </v-card>

    <!-- 지도 섹션 -->
    <v-card class="my-6" outlined>
      <BankMap :bank="product.kor_co_nm" />
    </v-card>

    <!-- 댓글 섹션 -->
    <v-card class="my-6" outlined>
      <v-card-title class="text-h6 font-weight-bold">댓글</v-card-title>
      <v-list dense>
        <v-list-item v-for="(comment, index) in comments" :key="index">
          <v-list-item-content>
            <v-list-item-subtitle class="text-body-2">{{ comment.content }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-textarea
        v-model="newComment"
        outlined
        dense
        rows="3"
        label="댓글을 입력하세요"
        class="mb-4"
        style="border-radius: 12px; background-color: #fff; box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1)"
      ></v-textarea>

      <!-- 댓글 등록 버튼 -->
      <div class="d-flex justify-end">
        <v-btn color="primary" class="font-weight-bold px-4 py-2" style="border-radius: 8px" @click="addComment" :disabled="newComment.trim() === ''">등록</v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<script setup>
import BankMap from "@/components/BankMap.vue";
import { useFinStore } from "@/stores/financial";
import { productCommentStore as useProductCommentStore } from "@/stores/product_comment";
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

const store = useFinStore();
const product = store.selectedProduct;
const productCommentStore = useProductCommentStore();
const route = useRoute();

const comments = ref([]); // 댓글 리스트
const newComment = ref(""); // 새로운 댓글 입력 필드

// 댓글 추가 함수
const addComment = async () => {
  if (newComment.value.trim() === "") {
    alert("댓글을 입력하세요");
    return;
  }
  await productCommentStore.createComment(product.id, newComment.value.trim());
  newComment.value = "";
};

// 상품 상세 정보
const productDetails = [
  { label: "상품 코드", value: product.fin_prdt_cd },
  { label: "금융사 코드", value: product.fin_co_no },
  { label: "가입 대상", value: product.join_member },
  { label: "가입 방법", value: product.join_way },
  { label: "특별 조건", value: product.spcl_cnd },
];

watch(
  () => productCommentStore.comment,
  (newComments) => {
    comments.value = newComments;
  },
  { immediate: true }
);
</script>

<style scoped>
.v-card {
  border-radius: 16px;
}
</style>
