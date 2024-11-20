<template>
  <v-container style="margin-top: 64px">
    <!-- 본문 내용 -->
    <div v-if="article">
      <!-- 본문 내용 -->
      <v-card flat class="pa-6 mb-6" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1)">
        <div class="d-flex align-center mb-4">
          <h1 class="text-h5 font-weight-bold mb-2" style="color: #222">{{ article.title }}</h1>
          <v-btn v-if="isOwner" color="primary" class="ml-auto px-4 py-2" small @click="openEditModal">
            <v-icon small left>mdi-pencil</v-icon>
            수정
          </v-btn>
          <v-btn v-else disabled class="ml-auto px-4 py-2" small>
            <v-icon small left>mdi-pencil</v-icon>
            수정 불가
          </v-btn>
        </div>
        <h2 class="text-subtitle-1 font-weight-medium mb-3" style="color: #555">{{ article.nickname }}</h2>
        <p style="color: #444; font-size: 16px; line-height: 1.8">{{ article.content }}</p>
      </v-card>

      <!-- 댓글 제목 -->
      <h2 v-if="comment.length > 0" class="text-h6 font-weight-bold mb-4" style="color: #222; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px">댓글 {{ comment.length }}개</h2>
      <h2 v-else class="text-h6 font-weight-bold mb-4" style="color: #666">작성된 댓글이 없어요...</h2>

      <!-- 댓글 리스트 -->
      <v-card flat class="pa-6 mb-6" style="background-color: #f8f9fa; border-radius: 12px; box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.05)">
        <div v-for="(item, index) in comment" :key="index" class="mb-4">
          <div v-if="item.is_deleted" style="color: #999; font-size: 14px">삭제된 댓글입니다.</div>
          <div v-else>
            <div class="d-flex align-center mb-2">
              <span class="font-weight-bold" style="color: #444; font-size: 14px">{{ item.nickname }}</span>
              <div v-if="isOwner" class="ml-auto d-flex align-center">
                <v-btn icon small @click="toggleEditMode(index)">
                  <v-icon small color="primary">mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon small @click="deleteComment(route.params.id, item.id)">
                  <v-icon small color="red">mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>
            <div class="pl-5" style="color: #555; font-size: 14px; line-height: 1.6">{{ item.content }}</div>

            <v-textarea v-if="editIndex === index" v-model="editedComment" outlined dense rows="2" label="수정할 내용을 입력하세요" class="mt-2" style="border-radius: 8px"></v-textarea>
            <v-btn v-if="editIndex === index" color="primary" class="mt-2" small @click="saveEdit(route.params.id, item.id)">수정 완료</v-btn>
            <v-btn v-if="editIndex === index" color="grey" class="mt-2 ml-2" small @click="cancelEdit">취소</v-btn>
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
        style="border-radius: 12px; background-color: #ffffff; box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.05)"
        :disabled="!isLogin"
      ></v-textarea>

      <!-- 댓글 등록 버튼 -->
      <div class="d-flex justify-end">
        <v-btn color="primary" class="font-weight-bold px-6 py-3" style="border-radius: 8px" :disabled="newComment.trim() === '' || !isLogin" @click="onCommentClick">댓글 등록</v-btn>
      </div>
    </div>

    <v-dialog v-model="editModal" max-width="500">
      <v-card>
        <v-card-title>
          <span class="text-h6">게시글 수정</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeEditModal">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="editedTitle" label="제목" outlined dense></v-text-field>
          <v-textarea v-model="editedContent" label="내용" outlined dense rows="5"></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="updateArticle">수정</v-btn>
          <v-btn color="grey" @click="closeEditModal">취소</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useAccount } from "@/stores/accounts";
import { commentStore } from "@/stores/comment";
import axios from "axios";

const accountStore = useAccount();
const store = commentStore();
const route = useRoute();

const article = ref(null);
const comment = ref([]);
const newComment = ref("");
const editModal = ref(false);
const editedTitle = ref("");
const editedContent = ref("");

// 사용자 확인
const isLogin = accountStore.isLogin;
const isOwner = computed(() => accountStore.user && accountStore.user === article.value?.user);

// 댓글 추가
const onCommentClick = () => {
  if (!isLogin) {
    accountStore.showLoginModal = true;
    return;
  }
  addComment();
};

const addComment = async () => {
  if (newComment.value.trim() === "") {
    alert("댓글을 입력하세요.");
    return;
  }
  try {
    await store.createComment(route.params.id, newComment.value.trim());
    newComment.value = ""; // 입력창 초기화
  } catch (error) {
    console.error("댓글 추가 실패:", error);
  }
};

// 데이터 로딩
onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/articles/${route.params.id}/`);
    article.value = response.data;
    store.getComments(route.params.id);
  } catch (error) {
    console.error("게시글 로딩 실패:", error);
  }
});

watch(
  () => store.comments,
  (newComments) => {
    comment.value = newComments;
  },
  { immediate: true }
);

// 댓글 수정/삭제 관련 로직 생략 (위 코드 참고)
</script>

<style scoped>
h1,
h2 {
  font-family: "Pretendard", sans-serif;
  color: #333;
}

.v-card {
  border-radius: 12px;
}

.v-btn {
  font-size: 14px;
  text-transform: none;
}

.v-textarea {
  font-size: 14px;
  padding: 12px;
}
</style>
