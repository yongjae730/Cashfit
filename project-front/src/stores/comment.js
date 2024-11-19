import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useAccount } from "./accounts";

export const commentStore = defineStore(
  "comments",
  () => {
    const comments = ref([]);
    const accountStore = useAccount();
    const token = accountStore.token;

    const API_URL = "http://127.0.0.1:8000";

    // 댓글 가져오기
    const getComments = function (articleId) {
      axios({
        method: "get",
        url: `${API_URL}/api/articles/${articleId}/`,
      })
        .then((res) => {
          comments.value = res.data.comments;
        })
        .catch((error) => console.log(error));
    };

    // 댓글 생성
    const createComment = function (articleId, content) {
      axios({
        method: "post",
        url: `${API_URL}/api/articles/${articleId}/comments/create/`,
        data: {
          content: content,
        },
        headers: {
          Authorization: `Token ${token}`,
        },
      })
        .then((res) => {
          comments.value.push(res.data);
        })
        .catch((error) => console.error("댓글 생성 실패:", error));
    };

    // 댓글 삭제 (isDelete = true로 설정)
    const deleteComment = async (articleId, commentId) => {
      try {
        await axios.delete(`${API_URL}/api/articles/${articleId}/comments/${commentId}/update-delete/`, {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
        });

        // 로컬 상태 업데이트
        const index = comments.value.findIndex((comment) => comment.id === commentId);
        if (index !== -1) {
          comments.value[index].isDelete = true;
        }
      } catch (error) {
        console.error("댓글 삭제 실패:", error);
      }
    };

    // 댓글 수정
    const updateComment = async (articleId, commentId, updatedContent) => {
      try {
        const response = await axios.put(
          `${API_URL}/api/articles/${articleId}/comments/${commentId}/update-delete/`,
          { content: updatedContent },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        // 로컬 상태 업데이트
        const index = comments.value.findIndex((comment) => comment.id === commentId);
        if (index !== -1) {
          comments.value[index].content = response.data.content;
        }
      } catch (error) {
        console.error("댓글 수정 실패:", error);
      }
    };

    return { API_URL, comments, getComments, createComment, deleteComment, updateComment };
  },
  { persist: true }
);
