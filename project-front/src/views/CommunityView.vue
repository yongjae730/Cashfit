<template>
  <v-container style="margin-top: 64px">
    <div class="d-flex justify-space-between align-center mb-4">
      <!-- 게시판 제목 -->
      <h1 class="page-title">게시판</h1>
      <!-- 게시글 작성 버튼 -->
      <v-btn color="primary" class="font-weight-bold" style="border-radius: 8px; color: white; font-size: 16px" @click="goToCreateArticle">게시글 작성</v-btn>
    </div>

    <!-- 게시판 테이블 -->
    <v-data-table :headers="headers" :items="paginatedArticles" class="elevation-1" dense>
      <template v-slot:item.id="{ item }">
        {{ item.id }}
      </template>
      <template v-slot:item.title="{ item }">
        <a href="#" style="color: #1976d2">{{ item.title }}</a>
      </template>
      <template v-slot:item.user="{ item }">
        {{ item.user }}
      </template>
      <template v-slot:item.create_at="{ item }">
        {{ item.create_at | formatDate }}
      </template>
      <template v-slot:item.updated_at="{ item }">
        {{ item.updated_at | formatDate }}
      </template>
    </v-data-table>

    <!-- 페이지네이션 -->
    <v-pagination v-model="currentPage" :length="pageCount" class="mt-4" color="primary"></v-pagination>
  </v-container>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

// Vue Router 설정
const router = useRouter();
const goToCreateArticle = () => {
  router.push({ name: "createArticle" });
};

// ArticleStore 활용
const ArticleStore = useArticleStore();
const articles = ref([]);

// 테이블 헤더
const headers = [
  { text: "No", value: "id", align: "start" },
  { text: "제목", value: "title" },
  { text: "글쓴이", value: "user" },
  { text: "작성시간", value: "create_at" },
  { text: "수정시간", value: "updated_at" },
];

// 페이지네이션 설정
const itemsPerPage = 5;
const currentPage = ref(1);

// 페이지네이션된 데이터 계산
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return articles.value.slice(start, end);
});

// 전체 페이지 수 계산
const pageCount = computed(() => Math.ceil(articles.value.length / itemsPerPage));

// onMounted 시 데이터 로드
onMounted(async () => {
  articles.value = await ArticleStore.articles; // Store에서 데이터 가져오기
});
</script>

<style scoped>
.page-title {
  font-size: 24px;
  color: #333;
  margin-bottom: 24px;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
}

a {
  text-decoration: none;
  font-weight: bold;
}

a:hover {
  text-decoration: underline;
}
</style>
