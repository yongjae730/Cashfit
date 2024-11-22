<template>
  <v-main class="bg-grey-lighten-4 pa-6" style="margin-top: 30px">
    <v-container>
      <!-- 상단 타이틀 카드 -->
      <v-card class="mb-6 rounded-lg" elevation="1">
        <div class="d-flex align-center pa-4 gradient-background">
          <v-icon icon="mdi-bitcoin" size="x-large" color="amber-darken-2" class="mr-4" />
          <div>
            <h1 class="text-h4 font-weight-bold text-white mb-1">코인 거래소</h1>
            <p class="text-grey-lighten-3 mb-0">실시간 암호화폐 시세 및 차트</p>
          </div>
        </div>
      </v-card>

      <!-- 메인 데이터 테이블 카드 -->
      <v-card elevation="1" class="rounded-lg">
        <v-card-text class="pa-0">
          <v-table fixed-header height="600px">
            <thead>
              <tr>
                <th class="text-left py-4 pl-6 text-h6 font-weight-bold">코인명</th>
                <th class="text-right py-4 pr-6 text-h6 font-weight-bold">현재가</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="coin in coins" :key="coin.code" class="hover-row" @click="openChart(coin)">
                <td class="pl-6">
                  <div class="d-flex align-center">
                    <v-chip :color="getRandomColor(coin.code)" label size="small" class="mr-3 font-weight-bold" variant="outlined">
                      {{ coin.code.replace("KRW-", "") }}
                    </v-chip>
                    <span class="font-weight-medium">{{ coin.name }}</span>
                  </div>
                </td>
                <td class="text-right pr-6">
                  <div>
                    <span class="text-h6 font-weight-bold">
                      {{ Number(coin.price).toLocaleString() }}
                    </span>
                    <span class="text-grey-darken-1 ml-1 text-body-2">KRW</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
    </v-container>

    <!-- 차트 다이얼로그 -->
    <v-dialog v-model="showChart" width="1000" height="700" @update:model-value="handleDialogClose" transition="dialog-bottom-transition">
      <v-card class="rounded-lg">
        <v-toolbar :color="getRandomColor(selectedCoin?.code)" prominent class="px-4">
          <template v-if="selectedCoin">
            <v-chip label size="large" variant="outlined" class="mr-3 font-weight-bold text-white" border>
              {{ selectedCoin.code.replace("KRW-", "") }}
            </v-chip>
            <div>
              <div class="text-h5 font-weight-bold text-white mb-1">
                {{ selectedCoin.name }}
              </div>
              <div class="text-grey-lighten-3">{{ Number(selectedCoin.price).toLocaleString() }} KRW</div>
            </div>
          </template>
          <template v-slot:append>
            <v-btn icon="mdi-close" variant="text" color="white" @click="showChart = false"></v-btn>
          </template>
        </v-toolbar>

        <v-card-text class="pa-6">
          <v-btn-group variant="outlined" class="mb-6 rounded-lg" divided>
            <v-btn v-for="interval in intervals" :key="interval.value" :color="selectedInterval === interval.value ? 'primary' : undefined" @click="changeInterval(interval.value)" class="px-6">
              {{ interval.label }}
            </v-btn>
          </v-btn-group>

          <div ref="chartContainer" class="rounded-lg overflow-hidden" style="height: 500px"></div>
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
    console.error("Error fetching market names:", error);
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
    console.error("캔들 데이터 조회 실패:", error);
  }
};

const connectWebSocket = () => {
  socket = new WebSocket("wss://api.upbit.com/websocket/v1");

  socket.onopen = () => {
    console.log("WebSocket connected!");
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
      console.error("JSON 파싱 에러:", error);
    }
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  socket.onclose = () => {
    console.log("WebSocket closed!");
  };
};

const connectChartWebSocket = () => {
  if (chartSocket) {
    chartSocket.close();
  }

  chartSocket = new WebSocket("wss://api.upbit.com/websocket/v1");
  chartSocket.binaryType = "blob";

  chartSocket.onopen = () => {
    console.log("Chart WebSocket connected!");
    const codes = [selectedCoin.value.code];
    chartSocket.send(JSON.stringify([{ ticket: "CHART_SOCKET" }, { type: "trade", codes }]));
  };

  chartSocket.onmessage = async (event) => {
    try {
      const text = await event.data.text();
      const data = JSON.parse(text);
      updateRealtimeCandle(data);
    } catch (error) {
      console.error("Chart WebSocket 파싱 에러:", error);
    }
  };

  chartSocket.onerror = (error) => {
    console.error("Chart WebSocket error:", error);
  };

  chartSocket.onclose = () => {
    console.log("Chart WebSocket closed!");
  };
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
.gradient-background {
  background: linear-gradient(135deg, #1867c0 0%, #5cbbf6 100%);
}

.hover-row {
  cursor: pointer;
  transition: all 0.2s ease;
}

.hover-row:hover {
  background-color: rgb(var(--v-theme-primary), 0.05) !important;
}

/* 차트 컨테이너 스타일 */
:deep(.tv-lightweight-charts) {
  border-radius: 8px;
  overflow: hidden;
}

/* 버튼 그룹 호버 효과 */
.v-btn-group .v-btn:hover {
  background-color: rgb(var(--v-theme-primary), 0.1);
}

/* 테이블 스타일링 */
:deep(.v-table) {
  background: transparent !important;
}

:deep(.v-table__wrapper) {
  border-radius: 8px;
}

:deep(.v-table > .v-table__wrapper > table) {
  background: transparent !important;
}

:deep(.v-table > .v-table__wrapper > table > thead > tr > th) {
  background: white !important;
  color: #1a237e !important;
}

:deep(.v-table > .v-table__wrapper > table > tbody > tr:not(:last-child) > td) {
  border-bottom: thin solid rgba(var(--v-border-color), 0.2) !important;
}

/* 다이얼로그 트랜지션 */
.dialog-bottom-transition-enter-active,
.dialog-bottom-transition-leave-active {
  transition: transform 0.3s ease-in-out;
}

.dialog-bottom-transition-enter-from,
.dialog-bottom-transition-leave-to {
  transform: translateY(100%);
}
</style>
