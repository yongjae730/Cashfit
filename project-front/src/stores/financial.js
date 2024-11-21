import axios from "axios";

import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useFinStore = defineStore(
  "financial",
  () => {
    const fin = ref([]);
    const selectedProduct = ref(null);
    const API_URL = "http://127.0.0.1:8000";

    const getFins = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/financials/financial-products/`,
      })
        .then((res) => {
          console.log(res.data);
          fin.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const setSelectedProduct = function (product) {
      selectedProduct.value = product;
    };

    const clearSelectedProduct = function () {
      selectedProduct.value = null;
    };

    return { API_URL, getFins, fin, selectedProduct, setSelectedProduct, clearSelectedProduct };
  },
  { persist: true }
);
