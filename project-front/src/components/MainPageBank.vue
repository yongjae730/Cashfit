<template>
  <div class="map-container">
    <h2 class="section-title">은행 어디로 가야하지??</h2>
    <div class="filter-section">
      <!-- 현재 위치 표시 및 초기화 버튼 -->
      <div class="current-location" v-if="accountStore.user?.user_info">
        <button @click="resetToUserLocation" class="reset-button" v-if="isLocationChanged">내 지역으로 돌아가기</button>
      </div>

      <!-- 시 / 도 선택 -->
      <v-select v-model="sido" :items="sidoList" label="시 / 도 선택" outlined dense class="select-box" @change="onSidoChange" :rules="[(v) => !!v || '시/도를 선택하세요']" />

      <!-- 구 / 군 선택 -->
      <v-select v-model="sigugun" :items="sigugunList" label="구 / 군 선택" outlined dense class="select-box" :rules="[(v) => !!v || '구/군을 선택하세요']" />

      <!-- 은행 이름 입력 -->
      <v-text-field v-model="bank" label="은행 입력" outlined dense class="bank-input" :rules="[(v) => !!v || '은행 정보를 입력해주세요']" style="border-radius: 8px" />

      <!-- 검색 버튼 -->
      <v-btn @click="searchBranches" color="primary" class="search-button">검색</v-btn>
    </div>
    <div class="content-container">
      <div ref="mapContainer" class="map-view"></div>
      <div class="place-list" v-if="places.length > 0">
        <h2>검색 결과 ({{ places.length }})</h2>
        <div v-for="(place, index) in places" :key="place.id" class="place-item" @click="focusPlace(index)" @mouseover="highlightMarker(index)" @mouseleave="unhighlightMarker(index)">
          <h3>{{ place.place_name }}</h3>
          <p class="address">{{ place.address_name }}</p>
          <p class="phone">{{ place.phone || "전화번호 없음" }}</p>
          <div class="distance" v-if="place.distance">
            {{ formatDistance(place.distance) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAddressStore } from "@/stores/address";
import { useAccount } from "@/stores/accounts";
import { computed, onMounted, ref, watch } from "vue";

const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_API_KEY;
const addressStore = useAddressStore();
const accountStore = useAccount();

const sido = ref("");
const sigugun = ref("");
const places = ref([]);
const bank = ref(""); // 은행은 빈 값으로 초기화
const activeMarkerIndex = ref(null);
const isLocationChanged = ref(false);

const sidoList = computed(() => ["시 / 도 선택", ...addressStore.address_infos.map((info) => info.sido)]);
const sigugunList = computed(() => {
  const selectedSido = addressStore.address_infos.find((info) => info.sido === sido.value);
  return ["구 / 군 선택", ...(selectedSido ? selectedSido.sigungus : [])];
});

// 위치 변경 확인
const checkLocationChanged = () => {
  if (!accountStore.user?.user_info) return false;
  isLocationChanged.value = sido.value !== accountStore.user.user_info.sido || sigugun.value !== accountStore.user.user_info.sigungus;
};

// 사용자 위치로 초기화
const resetToUserLocation = () => {
  if (!accountStore.user?.user_info) return;

  sido.value = accountStore.user.user_info.sido;
  sigugun.value = accountStore.user.user_info.sigungus;
  isLocationChanged.value = false;
  if (bank.value) searchBranches();
};

const onSidoChange = () => {
  sigugun.value = null;
  checkLocationChanged();
};

// 거리 포맷팅 함수
const formatDistance = (distance) => {
  if (distance < 1000) {
    return `${distance}m`;
  }
  return `${(distance / 1000).toFixed(1)}km`;
};

// Kakao 지도 관련
const mapContainer = ref(null);
const mapInstance = ref(null);
const markers = ref([]);

onMounted(async () => {
  if (!KAKAO_API_KEY) {
    alert("Kakao API 키가 설정되지 않았습니다. .env 파일을 확인하세요.");
    return;
  }

  // 사용자 정보가 없으면 가져오기
  if (accountStore.isLogin && !accountStore.user) {
    await accountStore.getProfile();
  }

  // 사용자 정보가 있으면 초기 위치 설정
  if (accountStore.user?.user_info) {
    sido.value = accountStore.user.user_info.sido;
    sigugun.value = accountStore.user.user_info.sigungus;
    console.log("Setting initial location:", sido.value, sigugun.value);
  }

  loadKaKaoMap(mapContainer.value);
});

const loadKaKaoMap = (container) => {
  if (window.kakao && window.kakao.maps) {
    initMap(container);
    return;
  }

  const script = document.createElement("script");
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_API_KEY}&libraries=services&autoload=false`;
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
    level: 1,
  };

  mapInstance.value = new window.kakao.maps.Map(container, options);

  window.kakao.maps.event.addListener(mapInstance.value, "click", (mouseEvent) => {
    console.log(mouseEvent.latLng);
  });
};

// 마커 포커스 함수
const focusPlace = (index) => {
  const place = places.value[index];
  const moveLatLng = new window.kakao.maps.LatLng(place.y, place.x);
  mapInstance.value.setCenter(moveLatLng);

  // 해당 마커의 인포윈도우 열기
  if (markers.value[index]) {
    const marker = markers.value[index];
    marker.infoWindow.open(mapInstance.value, marker);
  }
};

// 마커 하이라이트 함수들
const highlightMarker = (index) => {
  activeMarkerIndex.value = index;
  if (markers.value[index]) {
    const marker = markers.value[index];
    marker.infoWindow.open(mapInstance.value, marker);
  }
};

const unhighlightMarker = (index) => {
  activeMarkerIndex.value = null;
  if (markers.value[index]) {
    const marker = markers.value[index];
    marker.infoWindow.close();
  }
};

const addMarker = (position, place) => {
  const marker = new window.kakao.maps.Marker({ position });
  marker.setMap(mapInstance.value);

  const infoWindow = new window.kakao.maps.InfoWindow({
    content: `<div style="padding:5px">${place.place_name}</div>`,
  });

  // 마커 객체에 인포윈도우 저장
  marker.infoWindow = infoWindow;

  window.kakao.maps.event.addListener(marker, "click", () => {
    infoWindow.open(mapInstance.value, marker);
  });

  markers.value.push(marker);
};

const adjustMapBounds = () => {
  if (markers.value.length === 0) return;
  const bounds = new window.kakao.maps.LatLngBounds();

  markers.value.forEach((marker) => {
    bounds.extend(marker.getPosition());
  });

  mapInstance.value.setBounds(bounds);
};

const searchBranches = () => {
  const ps = new window.kakao.maps.services.Places();
  const query = `${sido.value} ${sigugun.value} ${bank.value}`;

  checkLocationChanged();

  ps.keywordSearch(query, (data, status, pagination) => {
    if (status === window.kakao.maps.services.Status.OK) {
      // 기존 마커 제거
      markers.value.forEach((marker) => marker.setMap(null));
      markers.value = [];

      // 검색 결과 저장
      places.value = data;

      data.forEach((place) => {
        const position = new window.kakao.maps.LatLng(place.y, place.x);
        addMarker(position, place);
      });

      adjustMapBounds();
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      swal({
        title: "ㅠㅠ",
        text: "검색 결과가 없어요..",
        icon: "warning",
        button: "확인",
      });
      places.value = [];
    } else {
      swal({
        title: "헉!",
        text: "검색 중 오류가 발생했어요.",
        icon: "warning",
        button: "확인",
      });
      places.value = [];
    }
  });
};

// user 정보 변경 감지
watch(
  () => accountStore.user?.user_info,
  (newUserInfo) => {
    if (newUserInfo && (!sido.value || !sigugun.value)) {
      sido.value = newUserInfo.sido;
      sigugun.value = newUserInfo.sigungus;
    }
  },
  { immediate: true }
);

// 위치 변경 감지
watch([sido, sigugun], () => {
  checkLocationChanged();
});
</script>

<style scoped>
.map-container {
  background-color: #f9f9f9;
  width: 100%;
  max-width: 1200px;
  padding: 30px;
  margin: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.filter-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  align-items: center;
}

.current-location {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.reset-button {
  padding: 6px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  height: 40px;
  transition: background-color 0.2s;
}

.reset-button:hover {
  background-color: #45a049;
}

.select-box {
  flex: 1;
}

.bank-input {
  flex: 2;
}

.search-button {
  padding: 10px 20px;
  height: 40px;
  font-size: 14px;
  font-weight: bold;
}

.search-button:hover {
  background-color: #1557b0;
}

.content-container {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.map-view {
  flex: 1;
  height: 600px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #ddd;
}

.place-list {
  width: 300px;
  background: white;
  border-radius: 8px;
  border: 1px solid #ddd;
  padding: 16px;
  overflow-y: auto;
  max-height: 600px;
}

.place-list h2 {
  margin: 0 0 16px 0;
  font-size: 18px;
  color: #333;
}

.place-item {
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.place-item:last-child {
  border-bottom: none;
}

.place-item:hover {
  background-color: #f5f5f5;
}

.place-item h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #1a73e8;
}

.place-item .address {
  margin: 4px 0;
  font-size: 14px;
  color: #666;
}

.place-item .phone {
  margin: 4px 0;
  font-size: 14px;
  color: #888;
}

.place-item .distance {
  margin-top: 4px;
  font-size: 12px;
  color: #1a73e8;
}
</style>
