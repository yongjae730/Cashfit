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
          console.log(res.data);
          articles.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    return { API_URL, getArticles, articles };
  },
  { persist: true }
);
