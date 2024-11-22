<template>
  <v-main class="product-section">
    <!-- 금융 상품 테이블 -->
    <FinProductTable />
    <SavingProductTable />
  </v-main>
</template>

<script setup>
import FinProductTable from "./FinProductTable.vue";
import SavingProductTable from "./SavingProductTable.vue";
</script>

<style scoped>
/* .product-section {
  /* background-color: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  margin-top: 20px; */

/* .tab-item {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: 500;
  color: #4a5568;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
} */

/* .tab-item.active {
  color: #2b6cb0;
  border-bottom: 2px solid #2b6cb0;
} */
</style>
