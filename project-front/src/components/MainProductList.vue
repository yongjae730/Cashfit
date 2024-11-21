<template>
  <div>
    <h2 class="v-typography headline-medium">지금 핫 한 상품은?</h2>
    <v-row class="product-section">
      <v-col cols="6">
        <FinProductTable />
      </v-col>
      <v-col cols="6">
        <SavingProductTable />
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import FinProductTable from "./FinProductTable.vue";
import SavingProductTable from "./SavingProductTable.vue";
</script>

<style scoped>
.product-section {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  margin-top: 20px;
}
</style>
