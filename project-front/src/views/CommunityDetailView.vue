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

      <CommunityComment :comments="comments" :isLogin="isLogin" :userNickname="userNickname" @add-comment="addComment" @update-comment="updateComment" @delete-comment="deleteComment" />
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
    </div>
  </v-container>
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

// 댓글 작성자인지 확인

// 게시글 작성자인지 확인 및 설정
watchEffect(() => {
  if (article.value && accountStore.user?.user_info?.nickname) {
    isOwner.value = article.value.nickname === accountStore.user.user_info.nickname;
  }
});

const fetchComments = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/articles/${route.params.id}`);
    comments.value = response.data.comments;
  } catch (error) {
    console.error("댓글 데이터를 가져오는 중 오류 발생:", error);
  }
};

onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/articles/${route.params.id}/`);
    article.value = response.data;

    fetchComments();
  } catch (error) {
    console.error("게시글 또는 댓글 로딩 실패:", error);
    alert("데이터를 로드하는 중 문제가 발생했습니다.");
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
    comments.value = response.data ? [...comment.value, response.data] : comments.value;
  } catch (error) {
    console.error("댓글 추가 실패:", error);
    alert("댓글을 추가하는 중 문제가 발생했습니다. 다시 시도해주세요.");
  }
};

const updateComment = async ({ id, content }) => {
  if (!content.trim()) {
    alert("수정할 내용을 입력하세요.");
    return;
  }
  try {
    await store.updateComment(route.params.id, id, content);
    const targetComment = comment.value.find((c) => c.id === id);
    if (targetComment) {
      targetComment.content = content;
    } else {
      console.error("수정할 댓글을 찾지 못했습니다.");
    }
  } catch (error) {
    console.error("댓글 수정 실패:", error);
    alert("댓글을 수정하는 중 문제가 발생했습니다. 다시 시도해주세요.");
  }
};

const deleteComment = async (commentId) => {
  try {
    await store.deleteComment(route.params.id, commentId);
    const targetComment = comment.value.find((c) => c.id === commentId);
    if (targetComment) {
      targetComment.is_deleted = true;
    } else {
      console.error("삭제할 댓글을 찾지 못했습니다.");
    }
  } catch (error) {
    console.error("댓글 삭제 실패:", error);
    alert("댓글을 삭제하는 중 문제가 발생했습니다. 다시 시도해주세요.");
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
    alert("제목과 내용을 입력하세요.");
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
    closeEditModal();
  } catch (error) {
    console.error("게시글 수정 실패:", error);
    alert("게시글을 수정하는 중 문제가 발생했습니다. 다시 시도해주세요.");
  }
};

// 댓글 데이터 로드 및 실시간 반영
watchEffect(() => {
  comments.value = store.comments;
});
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
