import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useAccount } from "./accounts";

export const useProductCommentStore = defineStore("products_comments", () => {
  const comment = ref({});
  const accountStore = useAccount();
  const token = accountStore.token;

  const API_URL = "http://127.0.0.1:8000";

  // 댓글 가져오기
  const getComments = async (productId) => {
    try {
      const response = await axios.get(`${API_URL}/api/financials/financial-comment/${productId}/`);
      comment.value[productId] = response.data;
      return response.data; // 댓글 데이터를 반환
    } catch (error) {
      console.error("댓글 가져오기 실패:", error);
      return [];
    }
  };

  // 댓글 생성
  const createComment = async (productId, content) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/financials/financial-comment_create/${productId}/`,
        { content },
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );
      // 댓글 생성 후 반환
      return response.data;
    } catch (error) {
      console.error("댓글 생성 실패:", error);
      throw error;
    }
  };

  return { API_URL, comment, getComments, createComment };
});
