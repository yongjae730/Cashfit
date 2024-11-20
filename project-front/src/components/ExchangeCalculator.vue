<template>
  <v-dialog v-model="internalShow" persistent max-width="500px">
    <v-card>
      <v-card-title>
        <span class="text-h5 font-weight-bold">미니 환율 계산기</span>
        <v-spacer></v-spacer>
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text>
        <v-select v-model="conversionType" :items="conversionOptions" label="환율 종류" variant="outlined"></v-select>
        <v-row class="mt-4">
          <v-col cols="6">
            <v-select v-model="selectedCurrency" :items="availableCurrencies" label="국가 선택" variant="outlined"></v-select>
            <v-text-field v-model="amount" type="number" label="금액 입력" variant="outlined" class="mt-4"></v-text-field>
          </v-col>
          <v-col cols="6" class="d-flex align-center justify-center">
            <span class="text-h5 font-weight-bold">{{ convertedAmount }} 원</span>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <v-btn color="primary" block @click="calculate">환율 계산하기</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  show: Boolean,
  exchange: Object,
});

const emit = defineEmits(["update:show"]);

const internalShow = ref(props.show);

watch(
  () => props.show,
  (newVal) => {
    internalShow.value = newVal;
  }
);

const conversionOptions = ["외화현찰을 사는 경우", "외화현찰을 파는 경우"];
const availableCurrencies = ref([]);
const conversionType = ref(conversionOptions[0]);
const selectedCurrency = ref(null);
const amount = ref(0);
const convertedAmount = ref(0);

watch(
  () => props.exchange,
  (newExchange) => {
    if (newExchange) {
      selectedCurrency.value = newExchange.cur_nm;
    }
  },
  { immediate: true }
);

const close = () => {
  emit("update:show", false);
};

const calculate = () => {
  // 환율 데이터를 숫자로 변환 (쉼표 제거)
  const rawRate = conversionType.value === "외화현찰을 사는 경우" ? props.exchange.tts : props.exchange.ttb;
  const rate = parseFloat(rawRate.replace(/,/g, "")); // 쉼표 제거 후 숫자로 변환

  if (isNaN(rate) || amount.value <= 0) {
    convertedAmount.value = "잘못된 입력값입니다.";
    return;
  }

  // 계산
  convertedAmount.value = (amount.value * rate).toLocaleString("ko-KR", {
    minimumFractionDigits: 2, // 소수점 이하 2자리
    maximumFractionDigits: 2, // 소수점 이하 2자리
  });
};
</script>

<style scoped></style>
