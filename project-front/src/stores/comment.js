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
    const getComments = function (articleId) {
      axios({
        method: "get",
        url: `${API_URL}/api/articles/${articleId}/comments`,
      })
        .then((res) => {
          comments.value = res.data;
        })
        .catch((error) => console.log(error));
    };

    const createComment = function (articleId, content) {
      axios({
        method: "post",
        url: `${API_URL}/api/articles/${articleId}/comments/create/`,
        data: {
          content: content,
          users: accountStore.users,
        },
        headers: {
          Authorization: `Token ${token}`,
        },
      }).then((res) => {
        comments.value.push(res.data);
      });
    };
    return { API_URL, getComments, createComment };
  },
  { persist: true }
);
