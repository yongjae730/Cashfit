<template>
  <div class="map-container">
    <h1>일단 맵 테스트</h1>
    <div class="filter-section">
      <select v-model="selectedRegion" class="select-box">
        <option value="">지역 선택</option>
        <option v-for="region in regions" :key="region.code" :value="region.code">
          {{ region.name }}
        </option>
      </select>

      <select v-model="selectedBank" class="select-box">
        <option value="">은행 선택</option>
        <option v-for="bank in banks" :key="bank.code" :value="bank.code">
          {{ bank.name }}
        </option>
      </select>
      <button @click="searchBranches" class="search-button">검색</button>
    </div>
    <div ref="mapContainer" class="map-view"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_API_KEY;

// 필터 상태
const selectedRegion = ref("");
const selectedBank = ref("");

// 예시 데이터
const regions = ref([
  { code: "seoul", name: "서울" },
  { code: "busan", name: "부산" },
]);

const banks = ref([
  { code: "kb", name: "KB국민은행" },
  { code: "shinhan", name: "신한은행" },
]);

// Kakao 지도 관련
const mapContainer = ref(null);
const markers = ref([]);

onMounted(() => {
  if (!KAKAO_API_KEY) {
    alert("Kakao API 키가 설정되지 않았습니다. .env 파일을 확인하세요.");
    return;
  }
  loadKaKaoMap(mapContainer.value);
});

const loadKaKaoMap = (container) => {
  if (window.kakao && window.kakao.maps) {
    initMap(container);
    return;
  }

  const script = document.createElement("script");
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&autoload=false`;
  document.head.appendChild(script);

  script.onload = () => {
    window.kakao.maps.load(() => initMap(container));
  };

  script.onerror = () => {
    alert("Kakao Maps API를 로드할 수 없습니다.");
  };
};

const initMap = (container) => {
  const options = {
    center: new window.kakao.maps.LatLng(33.450701, 126.570667),
    level: 3,
  };

  const mapInstance = new window.kakao.maps.Map(container, options);

  // 마커 추가 함수
  const addMarker = (position) => {
    const marker = new window.kakao.maps.Marker({ position });
    marker.setMap(mapInstance);
    markers.value.push(marker);
  };

  // 기본 마커 추가
  addMarker(new window.kakao.maps.LatLng(33.450701, 126.570667));
};

// 검색 기능
const searchBranches = () => {
  const branches = [
    { name: "지점 A", lat: 37.5665, lng: 126.978, region: "seoul", bank: "kb" },
    { name: "지점 B", lat: 35.1796, lng: 129.0756, region: "busan", bank: "shinhan" },
  ];

  const filtered = branches.filter((branch) => (!selectedRegion.value || branch.region === selectedRegion.value) && (!selectedBank.value || branch.bank === selectedBank.value));

  // 기존 마커 제거
  markers.value.forEach((marker) => marker.setMap(null));
  markers.value = [];

  // 새 마커 추가
  filtered.forEach((branch) => {
    addMarker(new window.kakao.maps.LatLng(branch.lat, branch.lng));
  });
};
</script>

<style scoped>
.map-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.filter-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.select-box {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 150px;
  background-color: white;
}

.search-button {
  padding: 8px 20px;
  background-color: #1a73e8;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.search-button:hover {
  background-color: #1557b0;
}

.map-view {
  width: 100%;
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #ddd;
}
</style>
