<template>
  <v-container style="margin-top: 64px">
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="page-title">게시판</h1>
      <v-btn color="primary" class="font-weight-bold" style="border-radius: 8px; color: white; font-size: 16px" @click="goToCreateArticle">게시글 작성</v-btn>
    </div>

    <v-data-table :headers="headers" :items="paginatedArticles" class="elevation-1" dense>
      <template v-slot:item.id="{ item }">
        {{ item.id }}
      </template>
      <template v-slot:item.title="{ item }">
        <RouterLink :to="{ name: 'articleDetail', params: { id: item.id } }" style="color: #1976d2">{{ item.title }}</RouterLink>
      </template>
      <template v-slot:item.create_at="{ item }">
        {{ formatDate(item.create_at) }}
      </template>
      <template v-slot:item.update_at="{ item }">
        {{ formatDate(item.update_at) }}
      </template>
    </v-data-table>

    <v-pagination v-model="currentPage" :length="pageCount" class="mt-4" color="primary"></v-pagination>
  </v-container>
</template>

<script setup>
import { useArticleStore } from "@/stores/articles";
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const goToCreateArticle = () => {
  router.push({ name: "createArticle" });
};

const formatDate = (dateString) => {
  if (!dateString) return "";
  const options = { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" };
  return new Date(dateString).toLocaleString("ko-KR", options);
};

const ArticleStore = useArticleStore();
const articles = ref([]);

const headers = [
  { title: "No", key: "id", align: "start" },
  { title: "제목", key: "title" },
  { title: "작성시간", key: "create_at" },
  { title: "수정시간", key: "update_at" },
];

const itemsPerPage = 5;
const currentPage = ref(1);

const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return articles.value.slice(start, end);
});

const pageCount = computed(() => Math.ceil(articles.value.length / itemsPerPage));

onMounted(() => {
  ArticleStore.getArticles();
  watch(
    () => ArticleStore.articles,
    (newArticles) => {
      articles.value = newArticles;
    },
    { immediate: true }
  );
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
