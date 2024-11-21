<template>
  <v-container class="exchange-calculator">
    <h3>환율 계산기</h3>
    <v-row align="center" justify="center">
      <!-- From Currency -->
      <v-col cols="12" md="5">
        <v-select label="살 것" v-model="selectedFromCurrency" :items="exchangeOptions" item-title="label" item-value="value" outlined dense />
      </v-col>

      <!-- 양방향 화살표 버튼 -->
      <v-col cols="12" md="2" class="d-flex justify-center align-center">
        <v-btn icon @click="swapCurrencies" color="primary" class="mx-2">
          <v-icon>mdi-swap-horizontal</v-icon>
        </v-btn>
      </v-col>

      <!-- To Currency -->
      <v-col cols="12" md="5">
        <v-select label="줄 것" v-model="selectedToCurrency" :items="exchangeOptions" item-title="label" item-value="value" outlined dense />
      </v-col>
    </v-row>

    <!-- Buttons -->
    <v-row justify="end">
      <v-btn color="primary" @click="calculateBuy">내가 살때</v-btn>
      &nbsp;
      <v-btn color="primary" @click="calculateSell">내가 팔때</v-btn>
    </v-row>

    <!-- Amount Input -->
    <v-row>
      <v-col cols="12">
        <v-text-field label="Amount:" v-model.number="amount" outlined />
      </v-col>
      <v-col cols="12">
        <v-text-field :value="convertedAmount" outlined readonly />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, watchEffect } from "vue";

// Props 정의
const props = defineProps({
  exchangeInfos: {
    type: Array,
    default: () => [],
  },
});

// Computed: exchangeOptions
const exchangeOptions = computed(() =>
  props.exchangeInfos.map((info) => ({
    label: `${info.cur_nm} (${info.cur_unit})`,
    value: info.cur_unit,
  }))
);

// 초기값 설정
const selectedFromCurrency = ref(null);
const selectedToCurrency = ref(null);
const amount = ref(1);
const convertedAmount = ref(0);

// 숫자 포맷 함수
const formatNumber = (value) => {
  if (value === null || value === undefined) return "";
  return new Intl.NumberFormat("en-US").format(value);
};

// Exchange Rates 계산 (KRW 포함)
const exchangeRates = computed(() => {
  const rates = props.exchangeInfos.reduce((acc, info) => {
    acc[info.cur_unit] = {
      ttb: parseFloat(info.ttb.replace(/,/g, "")), // 매입율
      tts: parseFloat(info.tts.replace(/,/g, "")), // 판매율
    };
    return acc;
  }, {});
  rates["KRW"] = { ttb: 1, tts: 1 }; // KRW 기본값 추가
  return rates;
});

// WatchEffect로 초기값 보장
watchEffect(() => {
  if (exchangeOptions.value.length > 0) {
    selectedFromCurrency.value = "USD"; // From 통화를 미국 달러로 설정
    selectedToCurrency.value = "KRW"; // To 통화를 한국 원으로 설정
  }
});

// Swap Currencies
const swapCurrencies = () => {
  const temp = selectedFromCurrency.value;
  selectedFromCurrency.value = selectedToCurrency.value;
  selectedToCurrency.value = temp;
};

// Calculate Buy
const calculateBuy = () => {
  if (!selectedFromCurrency.value || !selectedToCurrency.value) {
    console.error("선택된 통화 정보가 없습니다.");
    return;
  }

  const fromRate = exchangeRates.value[selectedFromCurrency.value]?.tts;
  const toRate = exchangeRates.value[selectedToCurrency.value]?.tts;

  if (fromRate && toRate) {
    const result = (amount.value * fromRate) / toRate;
    convertedAmount.value = formatNumber(parseFloat(result.toFixed(2)));
  } else {
    console.error("환율 정보를 찾을 수 없습니다.", { fromRate, toRate });
  }
};

// Calculate Sell
const calculateSell = () => {
  if (!selectedFromCurrency.value || !selectedToCurrency.value) {
    console.error("선택된 통화 정보가 없습니다.");
    return;
  }

  const fromRate = exchangeRates.value[selectedFromCurrency.value]?.ttb;
  const toRate = exchangeRates.value[selectedToCurrency.value]?.ttb;

  if (fromRate && toRate) {
    const result = (amount.value * fromRate) / toRate;
    convertedAmount.value = formatNumber(parseFloat(result.toFixed(2)));
  } else {
    console.error("환율 정보를 찾을 수 없습니다.", { fromRate, toRate });
  }
};
</script>

<style scoped>
.exchange-calculator {
  max-width: 1200px; /* 캐러셀과 동일한 너비로 확장 */
  margin: 0 auto; /* 중앙 정렬 */
  padding: 20px;
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.mx-2 {
  margin-left: 8px;
  margin-right: 8px;
}
</style>
