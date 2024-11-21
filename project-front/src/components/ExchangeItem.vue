<template>
  <v-col cols="4">
    <v-card class="exchange-card" @click="handleClick">
      <v-img :src="`/flag/${exchange.cur_unit}.png`" alt="국기" width="210" height="32" />
      <div class="exchange-title">{{ exchange.cur_nm }} ({{ exchange.cur_unit }})</div>
      <div class="exchange-rate">매매기준율: {{ exchange.deal_bas_r }}</div>
      <div class="exchange-actions">
        <v-btn color="primary" @click.stop="handleClick">자세히 보기</v-btn>
      </div>
    </v-card>
  </v-col>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  exchange: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits();

const handleClick = () => {
  emit("show-details", props.exchange);
};
</script>

<style scoped>
/* Same styles as before */
.exchange-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  height: 240px; /* Fixed height */
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  text-align: center;
}

.exchange-card:hover {
  transform: translateY(-4px);
  box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.15);
}

.exchange-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.exchange-rate {
  font-size: 1rem;
  color: #555;
  margin-bottom: auto;
}

.exchange-actions {
  margin-top: auto;
}
</style>
