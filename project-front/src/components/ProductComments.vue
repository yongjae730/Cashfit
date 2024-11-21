<template>
  <v-card class="rounded-xl" elevation="2">
    <v-card-title class="text-h5 font-weight-bold pa-6">
      <v-icon color="primary" class="mr-2">mdi-comment-multiple</v-icon>
      댓글
    </v-card-title>

    <v-card-text class="pa-6">
      <!-- 댓글 리스트 -->
      <v-skeleton-loader v-if="loading" type="list-item" :loading="loading"></v-skeleton-loader>

      <v-list v-else-if="comments">
        <v-list-item v-for="(comment, index) in comments" :key="index" class="mb-4 rounded-lg" elevation="1">
          <v-list-item-content>
            <v-list-item-title class="py-2">
              {{ comment.content }}
            </v-list-item-title>
            <v-list-item-subtitle class="py-2">
              {{ comment.create_at }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-alert v-else type="info" variant="tonal" class="mb-4">아직 댓글이 없습니다. 첫 댓글을 작성해보세요!</v-alert>

      <!-- 댓글 입력 -->
      <v-textarea v-model="newComment" label="댓글을 입력하세요" variant="outlined" rows="3" class="mt-6 rounded-lg" hide-details :disabled="!isLogin"></v-textarea>

      <div class="d-flex justify-end mt-4">
        <v-btn color="primary" size="large" :disabled="newComment.trim() === '' || !isLogin" @click="addComment">
          <v-icon left class="mr-2">mdi-send</v-icon>
          등록
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useAccount } from "@/stores/accounts";
import { useProductCommentStore } from "@/stores/product_comment";

const props = defineProps({
  productId: {
    type: Number,
    required: true,
  },
});

const productCommentStore = useProductCommentStore();
const comments = ref([]); // 초기값 빈 배열로 설정
const newComment = ref("");
const isLogin = useAccount().isLogin;
const loading = ref(false); // 로딩 상태 추가

const fetchComments = async () => {
  loading.value = true; // 로딩 시작
  try {
    const _fetchedComments = await productCommentStore.getComments(props.productId);
    console.log(_fetchedComments);
    if (Array.isArray(_fetchedComments)) {
      comments.value = _fetchedComments;
    } else {
      console.error("댓글 데이터가 배열이 아님:", _fetchedComments);
    }
  } catch (error) {
    console.error("댓글 데이터를 가져오는 중 오류 발생:", error);
  } finally {
    loading.value = false; // 로딩 종료
  }
};

const addComment = async () => {
  if (!newComment.value.trim()) {
    alert("댓글을 입력하세요!");
    return;
  }
  try {
    const createdComment = await productCommentStore.createComment(props.productId, newComment.value.trim());
    if (!createdComment || !createdComment.content) {
      throw new Error("댓글 생성 실패");
    }
    // 새로운 댓글을 기존 댓글 리스트의 맨 앞에 추가
    comments.value = [createdComment, ...comments.value];
    newComment.value = ""; // 입력창 초기화
  } catch (error) {
    console.error("댓글 작성 중 오류 발생:", error);
  }
};

onMounted(() => {
  fetchComments();
});

watch(
  () => props.productId,
  () => {
    fetchComments(); // 데이터 초기화 없이 새로운 댓글 데이터 로드
  }
);
</script>

<style scoped>
.v-list-item {
  transition: background-color 0.2s;
}
.v-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
}
</style>
