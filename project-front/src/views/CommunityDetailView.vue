<template>
  <v-main class="bg-grey-lighten-4" style="margin-top: 64px">
    <v-container class="py-8">
      <div v-if="article">
        <!-- 본문 카드 -->
        <v-card class="article-card mb-8">
          <!-- 헤더 섹션 -->
          <div class="article-header pa-8">
            <div class="d-flex align-center mb-6">
              <div>
                <h1 class="text-h4 font-weight-bold mb-2">{{ article.title }}</h1>
                <div class="d-flex align-center">
                  <v-avatar size="32" color="primary" class="mr-3">
                    <span class="text-white">{{ article.nickname[0] }}</span>
                  </v-avatar>
                  <span class="text-subtitle-1 font-weight-medium text-grey-darken-1">
                    {{ article.nickname }}
                  </span>
                </div>
              </div>
              <v-btn v-if="isOwner" color="primary" class="ml-auto edit-btn" prepend-icon="mdi-pencil" variant="flat" @click="openEditModal">수정</v-btn>
              <v-btn v-else disabled class="ml-auto" prepend-icon="mdi-pencil" variant="flat">수정 불가</v-btn>
            </div>
          </div>

          <v-divider></v-divider>

          <!-- 본문 내용 -->
          <div class="article-content pa-8">
            <p class="text-body-1">{{ article.content }}</p>
          </div>
        </v-card>

        <!-- 댓글 섹션 -->
        <CommunityComment :comments="comments" :isLogin="isLogin" :userNickname="userNickname" @add-comment="addComment" @update-comment="updateComment" @delete-comment="deleteComment" />

        <!-- 수정 모달 -->
        <v-dialog v-model="editModal" max-width="600">
          <v-card class="edit-modal">
            <v-card-title class="pa-6 bg-primary">
              <span class="text-h6 text-white">게시글 수정</span>
              <v-btn icon="mdi-close" variant="text" color="white" @click="closeEditModal"></v-btn>
            </v-card-title>

            <v-card-text class="pa-6">
              <v-text-field v-model="editedTitle" label="제목" variant="outlined" class="mb-4" density="comfortable"></v-text-field>

              <v-textarea v-model="editedContent" label="내용" variant="outlined" rows="6" density="comfortable"></v-textarea>
            </v-card-text>

            <v-card-actions class="pa-6">
              <v-spacer></v-spacer>
              <v-btn color="grey" variant="text" @click="closeEditModal" class="mr-2">취소</v-btn>
              <v-btn color="primary" @click="updateArticle" elevation="0">수정하기</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </div>
    </v-container>
  </v-main>
</template>
<script setup>
import { ref, computed, onMounted, watchEffect } from "vue";
import { useRoute } from "vue-router";
import { useAccount } from "@/stores/accounts";
import { commentStore } from "@/stores/comment";
import CommunityComment from "@/components/CommunityComment.vue";
import axios from "axios";

const accountStore = useAccount();
const store = commentStore();
const route = useRoute();

const article = ref(null);
const comments = ref([]);
const editModal = ref(false);
const editedTitle = ref("");
const editedContent = ref("");

const isOwner = ref(false);
const isLogin = computed(() => accountStore.isLogin);

const userNickname = accountStore.user?.user_info.nickname;

// 댓글 작성자인지 확인

// 게시글 작성자인지 확인 및 설정
watchEffect(() => {
  if (article.value && accountStore.user?.user_info?.nickname) {
    isOwner.value = article.value.nickname === accountStore.user.user_info.nickname;
  }
});

const fetchComments = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/articles/${route.params.id}/`);
    comments.value = response.data.comments;
  } catch (error) {
    swal({
      title: "오류 발생",
      text: "댓글 로드 중 오류가 발생했어요..",
      icon: "error",
      button: "확인",
    });
  }
};

onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/articles/${route.params.id}/`);
    article.value = response.data;

    await fetchComments();
  } catch (error) {
    swal({
      title: "오류 발생",
      text: "데이터를 로드하는 중 문제가 발생했어요..",
      icon: "error",
      button: "확인",
    });
  }
});

// 댓글 추가

const addComment = async (content) => {
  if (!content.trim()) {
    alert("댓글 내용을 입력하세요.");
    return;
  }
  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/articles/${route.params.id}/comments/create/`, { content }, { headers: { Authorization: `Token ${accountStore.token}` } });
    comments.value = response.data ? [...comments.value, response.data] : comments.value;
  } catch (error) {
    swal({
      title: "오류 발생",
      text: "댓글 로드 중 오류가 발생했어요..",
      icon: "error",
      button: "확인",
    });
  }
};

const updateComment = async ({ id, content }) => {
  if (!content.trim()) {
    swal({
      title: "경고",
      text: "수정할 내용을 입력하세요.",
      icon: "warning",
      button: "확인",
    });
    return;
  }
  try {
    await store.updateComment(route.params.id, id, content);
    const targetComment = comments.value.find((c) => c.id === id);
    if (targetComment) {
      targetComment.content = content;
    } else {
      swal({
        title: "경고",
        text: "수정할 내용을 입력하세요.",
        icon: "warning",
        button: "확인",
      });
    }
  } catch (error) {
    swal({
      title: "실패",
      text: "댓글을 수정하는 중 문제가 발생했습니다. 다시 시도해주세요.",
      icon: "error",
      button: "확인",
    });
  }
};

const deleteComment = async (commentId) => {
  try {
    await store.deleteComment(route.params.id, commentId);
    const targetComment = comments.value.find((c) => c.id === commentId);
    if (targetComment) {
      targetComment.is_deleted = true;
    } else {
      swal({
        title: "실패",
        text: "삭제할 댓글을 찾지 못했어요...",
        icon: "error",
        button: "확인",
      });
    }
  } catch (error) {
    swal({
      title: "실패",
      text: "댓글을 삭제하는 중 문제가 발생했습니다. 다시 시도해주세요.",
      icon: "error",
      button: "확인",
    });
  }
};
const openEditModal = () => {
  editedTitle.value = article.value.title;
  editedContent.value = article.value.content;
  editModal.value = true;
};

const closeEditModal = () => {
  editModal.value = false;
};

const updateArticle = async () => {
  if (!editedTitle.value.trim() || !editedContent.value.trim()) {
    swal({
      title: "경고",
      text: "제목과 내용을 입력하세요.",
      icon: "warning",
      button: "확인",
    });
    return;
  }
  try {
    const payload = {
      title: editedTitle.value.trim(),
      content: editedContent.value.trim(),
    };
    await axios.put(`http://127.0.0.1:8000/api/articles/${route.params.id}/update-delete/`, payload, {
      headers: { Authorization: `Token ${accountStore.token}` },
    });
    article.value.title = editedTitle.value;
    article.value.content = editedContent.value;

    await swal({
      title: "수정 완료!",
      text: "게시글 수정이 성공적으로 완료 되었어요!!",
      icon: "success",
      button: "확인",
    });
    closeEditModal();
  } catch (error) {
    swal({
      title: "실패",
      text: "게시글을 수정하는 중 문제가 발생했습니다. 다시 시도해주세요.",
      icon: "error",
      button: "확인",
    });
  }
};

// 댓글 데이터 로드 및 실시간 반영
watchEffect(() => {
  comments.value = store.comments;
});
</script>

<style scoped>
.article-card {
  border-radius: 16px;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
  overflow: hidden;
}

.article-header {
  background: linear-gradient(to right, #ffffff, #f8f9fa);
}

.edit-btn {
  transition: all 0.3s ease;
  border-radius: 8px;
  font-weight: 500;
}

.edit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.article-content {
  line-height: 1.8;
  color: #2c3e50;
  font-size: 1.1rem;
}

.edit-modal {
  border-radius: 16px;
  overflow: hidden;
}

:deep(.v-field) {
  border-radius: 8px;
}

:deep(.v-field:hover) {
  border-color: var(--v-primary-base);
}

:deep(.v-card-title) {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.v-btn) {
  text-transform: none;
  font-weight: 500;
  letter-spacing: 0.5px;
}

:deep(.v-textarea textarea) {
  line-height: 1.6;
}

/* 댓글 영역 스타일링 */
:deep(.v-card) {
  border-radius: 16px;
  overflow: hidden;
}

:deep(.v-avatar) {
  border: 2px solid white;
}

/* 애니메이션 효과 */
.v-dialog-transition-enter-active,
.v-dialog-transition-leave-active {
  transition: all 0.3s ease;
}

.v-dialog-transition-enter-from,
.v-dialog-transition-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
