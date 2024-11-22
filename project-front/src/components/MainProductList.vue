<template>
  <div class="product-section-wrapper">
    <h2 class="section-title">지금 핫한 상품은?</h2>
    <v-row class="product-section">
      <v-col cols="12" md="6">
        <div class="product-card-wrapper">
          <FinProductTable />
        </div>
      </v-col>
      <v-col cols="12" md="6">
        <div class="product-card-wrapper">
          <SavingProductTable />
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import FinProductTable from "./FinProductTable.vue";
import SavingProductTable from "./SavingProductTable.vue";
</script>

<style scoped>
.product-section-wrapper {
  background-color: #f9f9f9;
  width: 100%;
  max-width: 1200px;
  padding: 30px;
  margin: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
}

.product-section {
  margin: -10px;
}

.product-card-wrapper {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin: 10px;
  height: 100%;
}

@media (max-width: 959px) {
  .product-section-wrapper {
    padding: 20px;
  }

  .section-title {
    font-size: 18px;
    margin-bottom: 16px;
  }
}
</style>
