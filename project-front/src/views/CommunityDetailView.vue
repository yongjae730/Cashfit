<template>
  <v-container style="margin-top: 64px">
    <!-- 본문 내용 -->
    <div v-if="article">
      <!-- 본문 내용 -->
      <v-card flat class="pa-4 mb-6" style="background-color: #fff; border-radius: 16px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1)">
        <h1 class="text-h5 font-weight-bold mb-4" style="color: #333">{{ article.title }}</h1>
        <h2 class="text-h5 font-weight-bold mb-4" style="color: #333">{{ article.nickname }}</h2>
        <v-btn color="primary" class="ml-auto" small @click="openEditModal">
          <v-icon small left>mdi-pencil</v-icon>
          수정
        </v-btn>
        <p style="color: #555; font-size: 16px; line-height: 1.6">
          {{ article.content }}
        </p>
      </v-card>

      <!-- 댓글 제목 -->
      <h2 class="text-h6 font-weight-bold mb-4" style="color: #333">댓글 {{ comment.length }} 개</h2>

      <!-- 댓글 리스트 -->
      <v-card flat class="pa-4 mb-6" style="background-color: #f9fafc; border-radius: 16px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1)">
        <div v-for="(item, index) in comment" :key="index" class="mb-4">
          <!-- 삭제된 댓글 처리 -->
          <div v-if="item.is_deleted" style="color: #999; font-size: 14px">삭제된 댓글입니다.</div>
          <!-- 일반 댓글 -->
          <div v-else>
            <div class="d-flex align-center mb-2">
              <span class="font-weight-bold" style="color: #555">{{ item.nickname }}</span>
              <!-- 수정, 삭제 버튼 -->
              <div v-if="isOwner(item)" class="ml-auto d-flex align-center">
                <v-btn icon small @click="toggleEditMode(index)">
                  <v-icon small color="primary">mdi-pencil</v-icon>
                </v-btn>
                <v-btn icon small @click="deleteComment(route.params.id, item.id)">
                  <v-icon small color="red">mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>
            <!-- 댓글 텍스트 -->
            <div class="pl-5" style="color: #444; font-size: 14px">
              {{ item.content }}
            </div>

            <!-- 수정 입력창 -->
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
        style="border-radius: 12px; background-color: #fff; box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1)"
      ></v-textarea>

      <!-- 댓글 등록 버튼 -->
      <div class="d-flex justify-end">
        <v-btn color="primary" class="font-weight-bold px-4 py-2" style="border-radius: 8px" @click="addComment" :disabled="newComment.trim() === ''">등록</v-btn>
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
import { useArticleStore } from "@/stores/articles";
import { commentStore } from "@/stores/comment";
import axios from "axios";
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useAccount } from "@/stores/accounts";

const accountStore = useAccount(); // 사용자 정보 가져오기
const store = commentStore();
const articleStore = useArticleStore();
const route = useRoute();

const article = ref(null);
const comment = ref([]);
const newComment = ref("");

// 수정 모드 관련 상태
const editIndex = ref(null);
const editedComment = ref("");
const editModal = ref(false);
const editedTitle = ref("");
const editedContent = ref("");

const updateArticle = async () => {
  try {
    const payload = {
      title: editedTitle.value,
      content: editedContent.value,
    };
    await axios.put(`http://127.0.0.1:8000/api/articles/${route.params.id}/update-delete/`, payload, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    });
    article.value.title = editedTitle.value;
    article.value.content = editedContent.value;
    closeEditModal();
  } catch (error) {
    console.error("게시글 수정 실패:", error);
  }
};

// 모달 열기/닫기
const openEditModal = () => {
  editModal.value = true;
};

const closeEditModal = () => {
  editModal.value = false;
};

// 댓글 추가
const addComment = async () => {
  if (newComment.value.trim() === "") {
    alert("댓글을 입력하세요.");
    return;
  }
  await store.createComment(route.params.id, newComment.value.trim());
  newComment.value = ""; // 입력창 초기화
};

// 댓글 삭제
const deleteComment = async (articlePk, commentPk) => {
  const confirmDelete = confirm("댓글을 삭제하시겠습니까?");
  if (confirmDelete) {
    await store.deleteComment(articlePk, commentPk);
    const index = comment.value.findIndex((item) => item.id === commentPk);
    if (index !== -1) {
      comment.value[index].is_deleted = true; // 즉시 삭제 표시
    }
  }
};

// 수정 모드 토글
const toggleEditMode = (index) => {
  if (editIndex.value === index) {
    cancelEdit();
  } else {
    editIndex.value = index;
    editedComment.value = comment.value[index].content;
  }
};

// 수정 취소
const cancelEdit = () => {
  editIndex.value = null;
  editedComment.value = "";
};

// 수정 저장
const saveEdit = async (articlePk, commentPk) => {
  if (editedComment.value.trim() === "") {
    alert("내용을 입력하세요.");
    return;
  }
  await store.updateComment(articlePk, commentPk, editedComment.value.trim());
  comment.value[editIndex.value].content = editedComment.value.trim(); // 업데이트
  editIndex.value = null;
  editedComment.value = "";
};

// 댓글 데이터 가져오기
onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/articles/${route.params.id}/`);
    article.value = response.data;

    store.getComments(route.params.id);
  } catch (error) {
    console.error("게시글 로드 실패:", error);
  }
});

// 댓글 데이터 실시간 반영
watch(
  () => store.comments,
  (newComments) => {
    comment.value = newComments;
  },
  { immediate: true }
);

// 작성자 확인
const isOwner = (item) => {
  return accountStore.user === item.user; // 닉네임이 동일한지 확인
};
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
  min-width: 32px;
  height: 32px;
  margin-left: 4px;
  padding: 0;
}

.v-btn v-icon {
  font-size: 18px;
}

.v-textarea {
  max-width: 100%;
}

.v-avatar {
  font-size: 16px;
  font-weight: bold;
}
</style>
