<template>
  <v-container class="py-4">
    <!-- 본문 내용 -->
    <v-card flat class="pa-4 mb-6" style="background-color: #fff; border-radius: 16px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1)">
      <h1 class="text-h5 font-weight-bold mb-4" style="color: #333">{{ article.title }}</h1>
      <p style="color: #555; font-size: 16px; line-height: 1.6">
        {{ article.content }}
      </p>
    </v-card>

    <!-- 댓글 제목 -->
    <h2 class="text-h6 font-weight-bold mb-4" style="color: #333">댓글</h2>

    <!-- 댓글 리스트 -->
    <v-card flat class="pa-4 mb-6" style="background-color: #f9fafc; border-radius: 16px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1)">
      <div v-for="(comment, index) in commentStore.comments" :key="index" class="mb-4">
        <div class="d-flex align-center mb-2">
          <span class="font-weight-bold" style="color: #555">{{ comment.author }}</span>
          <!-- 삭제 버튼 -->
          <!-- <v-btn icon size="small" class="ml-auto" @click="deleteComment(articlePk, comment.id)" v-if="comment.isOwner">
            <v-icon>mdi-delete</v-icon>
          </v-btn> -->
        </div>
        <!-- 댓글 텍스트 -->
        <div class="pl-5" style="color: #444; font-size: 14px">
          {{ comment.text }}
        </div>
      </div>
    </v-card>

    <!-- 댓글 입력 -->
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
      <v-btn color="primary" class="font-weight-bold px-6" style="border-radius: 8px" @click="addComment" :disabled="newComment.trim() === ''">등록</v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { commentStore } from "@/stores/comment";
import { ref, onMounted } from "vue";

const store = commentStore();
const articlePk = 1; // 현재 게시글의 Primary Key (동적으로 설정 가능)

// 본문 데이터
const article = ref({
  title: "이 게시글의 제목입니다",
  content: "이곳은 게시글 본문 내용이 표시되는 영역입니다. 글의 내용은 여기에 나타나며, 다양한 정보를 포함할 수 있습니다.",
});

// 새 댓글
const newComment = ref("");

// 댓글 추가
const addComment = async () => {
  if (newComment.value.trim() === "") {
    alert("댓글을 입력하세요.");
    return;
  }
  await store.createComment(articlePk, newComment.value.trim());
  newComment.value = ""; // 입력창 초기화
};

// 댓글 삭제
const deleteComment = async (articlePk, commentPk) => {
  const confirmDelete = confirm("댓글을 삭제하시겠습니까?");
  if (confirmDelete) {
    await store.deleteComment(articlePk, commentPk);
  }
};

// 댓글 데이터 가져오기
onMounted(() => {
  store.getComments(articlePk);
});
</script>

<style scoped>
h1 {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
}

h2 {
  margin-bottom: 16px;
  color: #333;
}

.v-card {
  max-width: 100%;
  border-radius: 16px;
}

.v-btn {
  text-transform: none;
  font-size: 14px;
  font-weight: 600;
}

.v-textarea {
  max-width: 100%;
}

.v-avatar {
  font-size: 16px;
  font-weight: bold;
}
</style>
