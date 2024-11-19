<template>
  <v-container style="margin-top: 64px">
    <h1 class="page-title">게시판</h1>
    <!-- 게시판 테이블 -->
    <v-data-table :headers="headers" :items="paginatedItems" class="elevation-1" dense>
      <template #item.index="{ item }">
        {{ item.index }}
      </template>
      <template #item.title="{ item }">
        <a href="#" style="color: #1976d2">{{ item.title }}</a>
      </template>
    </v-data-table>

    <!-- 페이지네이션 -->
    <v-pagination v-model="currentPage" :length="pageCount" class="mt-4" color="primary"></v-pagination>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";

// 테이블 데이터 예시
const items = ref([
  { index: 10, title: "네이버 지도(v5) 임베드", author: "이은별", date: "2019-12-17" },
  { index: 9, title: "제목", author: "이은별", date: "2019-12-16" },
  { index: 8, title: "구글 지도 게시물에 임베드 하기", author: "이은별", date: "2019-12-16" },
  { index: 7, title: "아이폰 7 플러스", author: "이은별", date: "2018-05-14" },
  { index: 6, title: "분위기 좋네요~!", author: "이은별", date: "2018-04-17" },
  { index: 5, title: "진짜로 갑니다~~", author: "이은별", date: "2018-04-17" },
  { index: 4, title: "탑 메뉴 이미지", author: "이은별", date: "2017-12-06" },
  { index: 3, title: "응원합니다!", author: "이은별", date: "2017-11-20" },
  { index: 2, title: "이런건 기본이야아아아아아!", author: "이은별", date: "2017-11-20" },
  { index: 1, title: "제목만 보여주기", author: "이은별", date: "2017-11-20" },
]);

// 테이블 헤더
const headers = [
  { text: "No", value: "index", align: "start" },
  { text: "제목", value: "title" },
  { text: "글쓴이", value: "author" },
  { text: "작성시간", value: "date" },
];

// 페이지네이션 설정
const itemsPerPage = 5; // 한 페이지에 표시할 아이템 수
const currentPage = ref(1);

// 페이지에 표시할 데이터 계산
const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return items.value.slice(start, end);
});

// 전체 페이지 수 계산
const pageCount = computed(() => Math.ceil(items.value.length / itemsPerPage));
</script>

<style scoped>
h1 {
  font-size: 24px;
  color: #333;
  text-align: center;
}

a {
  text-decoration: none;
  font-weight: bold;
}

a:hover {
  text-decoration: underline;
}
.page-title {
  font-size: 24px; /* 글자 크기 */
  color: #333; /* 글자 색상 */
  text-align: center; /* 중앙 정렬 */
  margin-bottom: 24px; /* 아래 여백 추가 */
  line-height: 1.5; /* 줄 높이를 키워 잘리지 않도록 */
  white-space: nowrap; /* 텍스트가 줄 바꿈되지 않도록 */
  overflow: hidden; /* 부모 요소 밖으로 넘어가는 것을 방지 */
  text-overflow: ellipsis; /* 글자가 잘릴 경우 "..." 처리 */
}
</style>
