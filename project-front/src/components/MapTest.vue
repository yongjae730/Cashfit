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
      <button @clikc="searchBranches" class="search-button">검색</button>
    </div>
    <div ref="mapContainer" style="width: 100%; height: 500px"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_API_KEY;
const mapContainer = ref(null);
const markers = ref([]); // markers를 ref로 관리

onMounted(() => {
  if (!KAKAO_API_KEY) {
    console.error("Kakao API 키가 설정되지 않았습니다.");
    return;
  }
  loadKaKaoMap(mapContainer.value);
});

const loadKaKaoMap = (container) => {
  // 이미 로드되어 있는지 확인
  if (window.kakao && window.kakao.maps) {
    initMap(container);
    return;
  }

  const script = document.createElement("script");
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&autoload=false`;
  document.head.appendChild(script);

  script.onload = () => {
    window.kakao.maps.load(() => {
      const options = {
        center: new window.kakao.maps.LatLng(33.450701, 126.570667),
        level: 3,
        maxLevel: 5,
      };

      const mapInstance = new window.kakao.maps.Map(container, options);

      // 마커 추가 함수
      const addMarker = (position) => {
        const marker = new window.kakao.maps.Marker({
          position: position,
        });

        marker.setMap(mapInstance);
        markers.value.push(marker); // ref 값에 접근하기 위해 .value 사용
      };

      // 모든 마커 설정/해제 함수
      const setMarkers = (map) => {
        markers.value.forEach((marker) => {
          marker.setMap(map);
        });
      };

      // 초기 마커 추가
      addMarker(new window.kakao.maps.LatLng(33.450701, 126.570667));
      addMarker();
      // 마커 표시
      setMarkers(mapInstance);
    });
  };

  script.onerror = () => {
    console.error("Kakao Maps API를 로드할 수 없습니다.");
  };
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
  height: 600px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #ddd;
}
div[ref="mapContainer"] {
  width: 100%;
  height: 500px;
}
</style>
