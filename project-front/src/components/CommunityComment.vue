<template>
  <v-card flat class="pa-6 mb-6" style="background-color: #f8f9fa; border-radius: 12px; box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.05)">
    <!-- 댓글 제목 -->
    <h2 v-if="comments" class="text-h6 font-weight-bold mb-4" style="color: #222; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px">댓글 {{ comments.length }}개</h2>
    <h2 v-else class="text-h6 font-weight-bold mb-4" style="color: #666">작성된 댓글이 없어요...</h2>

    <!-- 댓글 리스트 -->
    <div v-for="(item, index) in comments" :key="index" class="mb-4">
      <div v-if="item.is_deleted" style="color: #999; font-size: 14px">삭제된 댓글입니다.</div>
      <div v-else>
        <div class="d-flex align-center mb-2">
          <span class="font-weight-bold" style="color: #444; font-size: 14px">{{ item.nickname }}</span>
          <div v-if="isCommentOwner(item)" class="ml-auto d-flex align-center">
            <v-btn icon small @click="toggleEditMode(index)">
              <v-icon small color="primary">mdi-pencil</v-icon>
            </v-btn>
            <v-btn icon small @click="$emit('delete-comment', item.id)">
              <v-icon small color="red">mdi-delete</v-icon>
            </v-btn>
          </div>
        </div>
        <div v-if="editIndex === index" class="pl-5">
          <v-textarea v-model="editedComment" outlined dense rows="2" label="수정할 내용을 입력하세요" class="mt-2" style="border-radius: 8px"></v-textarea>
          <v-btn color="primary" class="mt-2" small @click="saveEdit(item.id)">수정 완료</v-btn>
          <v-btn color="grey" class="mt-2 ml-2" small @click="cancelEdit">취소</v-btn>
        </div>
        <div v-else class="pl-5" style="color: #555; font-size: 14px; line-height: 1.6">{{ item.content }}</div>
      </div>
    </div>

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
      <v-btn color="primary" class="font-weight-bold px-6 py-3" style="border-radius: 8px" :disabled="!isLogin || newComment.trim() === ''" @click="addComment(newComment)">댓글 등록</v-btn>
    </div>
  </v-card>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  comments: {
    type: Array,
    required: true,
  },
  isLogin: {
    type: Boolean,
    required: true,
  },
  userNickname: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["add-comment", "update-comment", "delete-comment"]);

const newComment = ref("");
const editIndex = ref(null);
const editedComment = ref("");

// 댓글 작성
const addComment = () => {
  if (!newComment.value.trim()) {
    alert("댓글을 입력하세요.");
    return;
  }
  emit("add-comment", newComment.value.trim());
  newComment.value = ""; // 입력창 초기화
};

// 수정 모드 전환
const toggleEditMode = (index) => {
  if (editIndex.value === index) {
    cancelEdit();
  } else {
    editIndex.value = index;
    editedComment.value = props.comments[index].content;
  }
};

// 댓글 수정 취소
const cancelEdit = () => {
  editIndex.value = null;
  editedComment.value = "";
};

// 댓글 수정 완료
const saveEdit = (commentId) => {
  if (!editedComment.value.trim()) {
    alert("수정할 내용을 입력하세요.");
    return;
  }
  emit("update-comment", { id: commentId, content: editedComment.value.trim() });
  editIndex.value = null;
  editedComment.value = "";
};

// 댓글 작성자인지 확인
const isCommentOwner = (item) => {
  return props.userNickname && item.nickname === props.userNickname;
};
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}

.v-textarea {
  font-size: 14px;
  padding: 12px;
}
</style>
