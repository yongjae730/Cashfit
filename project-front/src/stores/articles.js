import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useArticleStore = defineStore(
  "article",
  () => {
    const articles = ref([]);

    const API_URL = "http://127.0.0.1:8000";
    const getArticles = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/articles/`,
      })
        .then((res) => {
          articles.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const createArticle = function (data) {
      axios({
        method: "post",
        url: `${API_URL}`,
        data: {
          data: data,
        },
      })
        .then((res) => {
          console.log(res.data);
          alert("게시글 생성 완료!");
        })
        .catch((err) => console.log(err));
    };

    return { API_URL, getArticles, articles };
  },
  { persist: true }
);
