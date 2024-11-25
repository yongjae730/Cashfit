<template>
  <v-main class="bg-grey-lighten-5 pa-6" style="margin-top: 30px">
    <v-container>
      <!-- 상단 타이틀 카드 -->
      <v-card class="mb-6 rounded-xl" elevation="2">
        <div class="d-flex align-center pa-6 premium-gradient">
          <v-avatar color="white" size="56" class="mr-6" elevation="2">
            <v-icon icon="mdi-bitcoin" size="32" color="amber-darken-2" />
          </v-avatar>
          <div>
            <h1 class="text-h4 font-weight-bold text-white mb-1">코인 거래소</h1>
            <p class="text-grey-lighten-4 mb-0 text-body-1">실시간 암호화폐 시세 및 차트</p>
          </div>
        </div>
      </v-card>

      <!-- 메인 데이터 테이블 카드 -->
      <v-card elevation="2" class="rounded-xl">
        <v-card-text class="pa-0">
          <v-table fixed-header height="600px" class="crypto-table">
            <thead>
              <tr>
                <th class="text-left py-5 pl-8 text-h6">코인명</th>
                <th class="text-right py-5 pr-8 text-h6">현재가</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="coin in coins" :key="coin.code" class="hover-row" @click="openChart(coin)">
                <td class="pl-8">
                  <div class="d-flex align-center py-3">
                    <v-chip :color="getRandomColor(coin.code)" label size="small" class="mr-4 font-weight-bold px-4" variant="flat">
                      {{ coin.code.replace("KRW-", "") }}
                    </v-chip>
                    <span class="font-weight-medium text-body-1">{{ coin.name }}</span>
                  </div>
                </td>
                <td class="text-right pr-8">
                  <div>
                    <span class="text-h6 font-weight-bold">
                      {{ Number(coin.price).toLocaleString() }}
                    </span>
                    <span class="text-grey-darken-1 ml-2">KRW</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
    </v-container>

    <!-- 차트 다이얼로그 -->
    <v-dialog v-model="showChart" width="1000" @update:model-value="handleDialogClose" transition="dialog-bottom-transition" class="rounded-xl">
      <v-card class="rounded-xl">
        <v-toolbar :color="getRandomColor(selectedCoin?.code)" prominent class="px-6 chart-toolbar">
          <template v-if="selectedCoin">
            <v-chip label size="large" variant="outlined" class="mr-4 font-weight-bold text-white pa-4" border>
              {{ selectedCoin.code.replace("KRW-", "") }}
            </v-chip>
            <div>
              <div class="text-h5 font-weight-bold text-white mb-1">
                {{ selectedCoin.name }}
              </div>
              <div class="text-grey-lighten-4 text-body-1">{{ Number(selectedCoin.price).toLocaleString() }} KRW</div>
            </div>
          </template>
          <template v-slot:append>
            <v-btn icon="mdi-close" variant="text" color="white" size="large"></v-btn>
          </template>
        </v-toolbar>

        <v-card-text class="pa-8">
          <v-btn-group variant="outlined" class="mb-8 rounded-lg custom-btn-group" divided>
            <v-btn
              v-for="interval in intervals"
              :key="interval.value"
              :color="selectedInterval === interval.value ? 'primary' : undefined"
              @click="changeInterval(interval.value)"
              class="px-6 py-2"
              elevation="0"
            >
              {{ interval.label }}
            </v-btn>
          </v-btn-group>

          <div ref="chartContainer" class="rounded-xl chart-container"></div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-main>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import axios from "axios";

// 상태 변수들
const coins = ref([]);
const showChart = ref(false);
const selectedCoin = ref(null);
const selectedInterval = ref("minute1");
const chartContainer = ref(null);
let chart = null;
let candleSeries = null;
let socket = null;
let chartSocket = null;
let currentCandle = null;

// TradingView 차트 라이브러리 로드
let tvScriptLoadingPromise;
onMounted(() => {
  tvScriptLoadingPromise = new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = "https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js";
    script.async = true;
    script.onload = resolve;
    document.head.appendChild(script);
  });
});

// 차트 간격 옵션
const intervals = [
  { label: "1분", value: "minute1" },
  { label: "3분", value: "minute3" },
  { label: "5분", value: "minute5" },
  { label: "15분", value: "minute15" },
  { label: "30분", value: "minute30" },
  { label: "60분", value: "minute60" },
];

// 유틸리티 함수
const getRandomColor = (code) => {
  const colors = ["primary", "secondary", "success", "info", "warning"];
  const hash = code.split("").reduce((acc, char) => char.charCodeAt(0) + acc, 0);
  return colors[hash % colors.length];
};

const getCurrentCandleTime = () => {
  const now = new Date();
  const minutes = now.getMinutes();
  const interval = parseInt(selectedInterval.value.replace("minute", ""));
  const candleMinutes = Math.floor(minutes / interval) * interval;

  const candleTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), candleMinutes, 0, 0);

  return Math.floor(candleTime.getTime() / 1000);
};

// 차트 관련 함수들
const initChart = async () => {
  await tvScriptLoadingPromise;

  if (chartContainer.value) {
    if (chart) {
      chart.remove();
    }

    chart = LightweightCharts.createChart(chartContainer.value, {
      layout: {
        background: { color: "#ffffff" },
        textColor: "#333",
      },
      grid: {
        vertLines: { color: "#f0f0f0" },
        horzLines: { color: "#f0f0f0" },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        rightOffset: 12,
        barSpacing: 12,
        fixLeftEdge: true,
        lockVisibleTimeRangeOnResize: true,
        rightBarStaysOnScroll: true,
        borderVisible: false,
      },
      crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
      },
    });

    candleSeries = chart.addCandlestickSeries({
      upColor: "#26a69a",
      downColor: "#ef5350",
      borderVisible: false,
      wickUpColor: "#26a69a",
      wickDownColor: "#ef5350",
    });

    const handleResize = () => {
      if (chart && chartContainer.value) {
        chart.applyOptions({
          width: chartContainer.value.clientWidth,
          height: chartContainer.value.clientHeight,
        });
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize();

    // 컴포넌트가 언마운트될 때 이벤트 리스너 제거
    onUnmounted(() => {
      window.removeEventListener("resize", handleResize);
    });
  }
};

const updateRealtimeCandle = (tradeData) => {
  if (!candleSeries || !currentCandle) return;

  const currentTime = getCurrentCandleTime();
  const tradePrice = tradeData.trade_price;

  if (currentTime > currentCandle.time) {
    const newCandle = {
      time: currentTime,
      open: tradePrice,
      high: tradePrice,
      low: tradePrice,
      close: tradePrice,
    };
    currentCandle = newCandle;
    candleSeries.update(newCandle);
  } else if (currentTime === currentCandle.time) {
    currentCandle.high = Math.max(currentCandle.high, tradePrice);
    currentCandle.low = Math.min(currentCandle.low, tradePrice);
    currentCandle.close = tradePrice;
    candleSeries.update(currentCandle);
  }
};

// API 및 WebSocket 관련 함수들
const fetchMarketNames = async () => {
  try {
    const response = await axios.get("https://api.upbit.com/v1/market/all");
    return response.data
      .filter((market) => market.market.startsWith("KRW-"))
      .map((market) => ({
        code: market.market,
        name: market.korean_name,
        price: 0,
      }));
  } catch (error) {
    swal({
      title: "실패",
      text: "데이터를 찾지 못했어요...",
      icon: "error",
      button: "확인",
    });
    return [];
  }
};

const fetchCandleData = async () => {
  if (!selectedCoin.value) return;

  try {
    const unit = selectedInterval.value.replace("minute", "");
    const response = await axios.get(`https://api.upbit.com/v1/candles/minutes/${unit}`, {
      params: {
        market: selectedCoin.value.code,
        count: 200,
      },
    });

    const candleData = response.data
      .map((candle) => ({
        time: Math.floor(candle.timestamp / 1000),
        open: candle.opening_price,
        high: candle.high_price,
        low: candle.low_price,
        close: candle.trade_price,
      }))
      .reverse();

    if (candleSeries) {
      candleSeries.setData(candleData);
      currentCandle = { ...candleData[candleData.length - 1] };

      const currentTime = getCurrentCandleTime();
      if (currentTime > currentCandle.time) {
        const lastPrice = currentCandle.close;
        currentCandle = {
          time: currentTime,
          open: lastPrice,
          high: lastPrice,
          low: lastPrice,
          close: lastPrice,
        };
        candleSeries.update(currentCandle);
      }
    }
  } catch (error) {
    swal({
      title: "실패",
      text: "데이터를 찾지 못했어요...",
      icon: "error",
      button: "확인",
    });
  }
};

const connectWebSocket = () => {
  socket = new WebSocket("wss://api.upbit.com/websocket/v1");

  socket.onopen = () => {
    const codes = coins.value.map((coin) => coin.code);
    socket.send(JSON.stringify([{ ticket: "UNIQUE_TICKET_ID" }, { type: "ticker", codes }]));
  };

  socket.onmessage = async (event) => {
    try {
      const text = await event.data.text();
      const data = JSON.parse(text);
      const coinIndex = coins.value.findIndex((coin) => coin.code === data.code);
      if (coinIndex !== -1) {
        coins.value[coinIndex].price = data.trade_price;
      }
    } catch (error) {
      swal({
        title: "실패",
        text: "데이터를 찾지 못했어요...",
        icon: "error",
        button: "확인",
      });
    }
  };

  socket.onerror = (error) => {
    swal({
      title: "실패",
      text: "데이터를 찾지 못했어요...",
      icon: "error",
      button: "확인",
    });
  };

  socket.onclose = () => {};
};

const connectChartWebSocket = () => {
  if (chartSocket) {
    chartSocket.close();
  }

  chartSocket = new WebSocket("wss://api.upbit.com/websocket/v1");
  chartSocket.binaryType = "blob";

  chartSocket.onopen = () => {
    const codes = [selectedCoin.value.code];
    chartSocket.send(JSON.stringify([{ ticket: "CHART_SOCKET" }, { type: "trade", codes }]));
  };

  chartSocket.onmessage = async (event) => {
    try {
      const text = await event.data.text();
      const data = JSON.parse(text);
      updateRealtimeCandle(data);
    } catch (error) {
      swal({
        title: "실패",
        text: "데이터를 찾지 못했어요...",
        icon: "error",
        button: "확인",
      });
    }
  };

  chartSocket.onerror = (error) => {
    swal({
      title: "실패",
      text: "데이터를 찾지 못했어요...",
      icon: "error",
      button: "확인",
    });
  };

  chartSocket.onclose = () => {};
};

// 이벤트 핸들러
const openChart = async (coin) => {
  selectedCoin.value = coin;
  showChart.value = true;
  await initChart();
  fetchCandleData();
  connectChartWebSocket();
};

const changeInterval = (interval) => {
  selectedInterval.value = interval;
  if (chartSocket) {
    chartSocket.close();
    chartSocket = null;
  }
  currentCandle = null;
  fetchCandleData();
  connectChartWebSocket();
};

const handleDialogClose = (value) => {
  if (!value) {
    if (chartSocket) {
      chartSocket.close();
      chartSocket = null;
    }
    if (chart) {
      chart.remove();
      chart = null;
    }
    currentCandle = null;
    candleSeries = null;
  }
};

// 컴포넌트 라이프사이클
onMounted(async () => {
  const marketNames = await fetchMarketNames();
  coins.value = marketNames;
  connectWebSocket();
});

onUnmounted(() => {
  if (socket) socket.close();
  if (chartSocket) chartSocket.close();
  if (chart) chart.remove();
});

// 다이얼로그 감시
watch(showChart, (newValue) => {
  if (!newValue && chart) {
    chart.remove();
    chart = null;
    candleSeries = null;
  }
});
</script>

<style scoped>
.premium-gradient {
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
}

.hover-row {
  cursor: pointer;
  transition: all 0.25s ease;
}

.hover-row:hover {
  background-color: rgba(var(--v-theme-primary), 0.04);
  transform: translateY(-1px);
}

/* 차트 관련 스타일 수정 */
.chart-container {
  height: 600px; /* 차트 높이 증가 */
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 16px;
  padding: 16px;
  background: linear-gradient(to bottom, #ffffff, #f8fafc);
}

.custom-btn-group {
  border: none;
  background-color: #f1f5f9;
  border-radius: 12px;
  padding: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.custom-btn-group .v-btn {
  font-weight: 600;
  letter-spacing: 0;
  text-transform: none;
  border: none !important;
  background-color: transparent;
  min-width: 80px;
  border-radius: 8px !important;
  height: 40px;
  font-size: 0.9rem;
}

.custom-btn-group .v-btn:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
  transform: translateY(-1px);
  transition: all 0.2s ease;
}

.custom-btn-group .v-btn.v-btn--active {
  background-color: white !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  color: #1a237e;
}

/* 차트 다이얼로그 스타일 개선 */
:deep(.v-dialog > .v-card) {
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2) !important;
}

.chart-toolbar {
  background: linear-gradient(to right, rgba(26, 35, 126, 0.95), rgba(13, 71, 161, 0.95)) !important;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  height: 90px !important;
}

:deep(.v-toolbar-title) {
  font-size: 1.5rem !important;
  font-weight: 700;
}

/* 차트 관련 칩 스타일 */
:deep(.v-chip) {
  font-size: 1rem;
  height: 36px;
  background: rgba(255, 255, 255, 0.15) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  backdrop-filter: blur(5px);
}

.crypto-table {
  border-collapse: separate;
  border-spacing: 0;
}

:deep(.v-table) {
  background: transparent !important;
}

:deep(.v-table__wrapper) {
  border-radius: 16px;
  box-shadow: none;
}

:deep(.v-table > .v-table__wrapper > table) {
  background: transparent !important;
}

:deep(.v-table > .v-table__wrapper > table > thead > tr > th) {
  background: white !important;
  color: #1a237e !important;
  font-weight: 600;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

:deep(.v-table > .v-table__wrapper > table > tbody > tr:not(:last-child) > td) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
}

/* 다이얼로그 트랜지션 개선 */
.dialog-bottom-transition-enter-active,
.dialog-bottom-transition-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.dialog-bottom-transition-enter-from,
.dialog-bottom-transition-leave-to {
  transform: translateY(50px);
  opacity: 0;
}

/* 닫기 버튼 스타일 */
:deep(.v-toolbar .v-btn--icon) {
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

:deep(.v-toolbar .v-btn--icon:hover) {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

/* 차트 컨테이너 내부 스타일 */
:deep(.tv-lightweight-charts) {
  border-radius: 12px;
  overflow: hidden;
}
</style>
