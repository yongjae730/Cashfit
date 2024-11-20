<template>
  <v-card elevation="2" class="rounded-lg pa-4" @click="viewDetail">
    <v-row align="center">
      <v-col cols="3">
        <v-img :src="`/flags/${exchange.cur_unit}.png`" alt="국기" width="48" height="32" />
      </v-col>
      <v-col cols="6">
        <div class="text-h6 font-weight-bold">{{ exchange.cur_nm }} ({{ exchange.cur_unit }})</div>
        <div class="text-subtitle-2">매매기준율: {{ exchange.deal_bas_r }}</div>
      </v-col>
      <v-col cols="3" class="text-right">
        <v-btn small>상세보기</v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup>
const props = defineProps({
  exchange: Object,
});

const emit = defineEmits(["view-detail"]);

const viewDetail = () => {
  emit("view-detail", props.exchange);
};
</script>

<style scoped></style>
