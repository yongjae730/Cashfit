import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useAccount } from "./accounts";

export const productCommentStore = defineStore(
  "comments",
  () => {
    const comment = ref([]);
    const accountStore = useAccount();
    const token = accountStore.token;

    const API_URL = "http://127.0.0.1:8000";

    // 댓글 가져오기
    const getComments = function (productId) {
      axios({
        method: "get",
        url: `${API_URL}/api/financials/financial-comment/${productId}`,
      })
        .then((res) => {
          comment.value = res.data;
        })
        .catch((error) => console.log(error));
    };

    // 댓글 생성
    const createComment = function (productId, content) {
      axios({
        method: "post",
        url: `${API_URL}/api/financials/financial-comment_create/${productId}/`,
        data: {
          content: content,
        },
        headers: {
          Authorization: `Token ${token}`,
        },
      })
        .then((res) => {
          console.log("댓글 생성 응답 데이터:", res.data);

          // comments.value가 제대로 초기화되어 있는지 확인하고 초기화
          if (!Array.isArray(comment.value)) {
            comment.value = [];
          }

          // 응답 데이터가 객체인지 확인하고 추가
          if (res.data && typeof res.data === "object" && res.data.id) {
            comment.value.push(res.data);
          } else {
            console.error("댓글 데이터가 예상한 형식이 아닙니다.");
          }
        })
        .catch((error) => {
          console.log(token);
          console.error("댓글 생성 실패:", error);

          // comments가 정의되지 않은 경우 빈 배열로 초기화
          if (!Array.isArray(comment.value)) {
            comment.value = [];
          }
        });
    };

    // // 댓글 삭제 (isDelete = true로 설정)
    // const deleteComment = async (articleId, commentId) => {
    //   try {
    //     await axios.delete(`${API_URL}/api/articles/${articleId}/comments/${commentId}/update-delete/`, {
    //       headers: {
    //         Authorization: `Token ${accountStore.token}`,
    //       },
    //     });

    //     // 로컬 상태 업데이트
    //     const index = comments.value.findIndex((comment) => comment.id === commentId);
    //     if (index !== -1) {
    //       comments.value[index].isDelete = true;
    //     }
    //   } catch (error) {
    //     console.error("댓글 삭제 실패:", error);
    //   }
    // };

    // // 댓글 수정
    // const updateComment = async (articleId, commentId, updatedContent) => {
    //   try {
    //     const response = await axios.put(
    //       `${API_URL}/api/articles/${articleId}/comments/${commentId}/update-delete/`,
    //       { content: updatedContent },
    //       {
    //         headers: {
    //           Authorization: `Token ${token}`,
    //         },
    //       }
    //     );

    //     // 로컬 상태 업데이트
    //     const index = comments.value.findIndex((comment) => comment.id === commentId);
    //     if (index !== -1) {
    //       comments.value[index].content = response.data.content;
    //     }
    //   } catch (error) {
    //     console.error("댓글 수정 실패:", error);
    //   }
    // };

    return { API_URL, comment, getComments, createComment };
  },
  { persist: true }
);
