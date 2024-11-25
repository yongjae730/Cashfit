<template>
  <v-main class="pa-6" style="margin-top: 40px; background-color: #f8f9fa">
    <v-container>
      <!-- 헤더 섹션 -->
      <v-card class="mb-6 rounded-xl" elevation="2">
        <div class="d-flex justify-space-between align-center pa-6 header-gradient">
          <div class="d-flex align-center">
            <v-avatar color="white" size="48" class="mr-4" elevation="1">
              <v-icon icon="mdi-forum" size="24" color="primary" />
            </v-avatar>
            <h1 class="text-h4 font-weight-bold text-white">게시판</h1>
          </div>
          <v-btn color="white" class="create-btn font-weight-bold px-6" elevation="2" prepend-icon="mdi-plus" @click="goToCreateArticle">게시글 작성</v-btn>
        </div>
      </v-card>

      <!-- 테이블 카드 -->
      <v-card class="rounded-xl" elevation="2">
        <v-data-table :headers="headers" :items="paginatedArticles" class="custom-table" dense>
          <template v-slot:item.id="{ item }">
            <div class="font-weight-medium">{{ item.id }}</div>
          </template>

          <template v-slot:item.title="{ item }">
            <RouterLink :to="{ name: 'articleDetail', params: { id: item.id } }" class="title-link d-inline-block">
              {{ item.title }}
            </RouterLink>
          </template>

          <template v-slot:item.create_at="{ item }">
            <div class="text-grey-darken-1">{{ formatDate(item.create_at) }}</div>
          </template>

          <template v-slot:item.update_at="{ item }">
            <div class="text-grey-darken-1">{{ formatDate(item.update_at) }}</div>
          </template>
        </v-data-table>

        <!-- 페이지네이션 -->
        <div class="pa-4 d-flex justify-center">
          <v-pagination v-model="currentPage" :length="pageCount" color="primary" rounded="circle" elevation="2"></v-pagination>
        </div>
      </v-card>
    </v-container>
  </v-main>
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

const itemsPerPage = 10;
const currentPage = ref(1);

// 정렬된 전체 게시글을 반환하는 computed 속성
const sortedArticles = computed(() => {
  return [...articles.value].sort((a, b) => {
    return new Date(b.create_at) - new Date(a.create_at);
  });
});

// paginatedArticles computed 속성
const paginatedArticles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return sortedArticles.value.slice(start, end);
});

const pageCount = computed(() => Math.ceil(sortedArticles.value.length / itemsPerPage));

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
.header-gradient {
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
}

.create-btn {
  transition: all 0.3s ease;
  border-radius: 12px;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

.title-link {
  color: #1a237e;
  text-decoration: none;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.title-link:hover {
  background-color: rgba(26, 35, 126, 0.05);
  text-decoration: none;
  color: #0d47a1;
}

:deep(.v-data-table) {
  background: transparent !important;
}

:deep(.v-data-table-header) {
  background-color: #f8f9fa !important;
}

:deep(.v-data-table-header th) {
  color: #1a237e !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 12px 16px !important;
}

:deep(.v-data-table-rows tr) {
  transition: background-color 0.2s ease;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
}

:deep(.v-data-table-rows tr:hover) {
  background-color: rgba(26, 35, 126, 0.02) !important;
}

:deep(.v-data-table-rows td) {
  padding: 12px 16px !important;
  font-size: 0.9rem !important;
}

:deep(.v-pagination__item) {
  box-shadow: none !important;
  font-weight: 500;
  transition: all 0.2s ease;
}

:deep(.v-pagination__item--is-active) {
  transform: scale(1.1);
}

.custom-table {
  border-radius: 12px;
  overflow: hidden;
}
</style>
