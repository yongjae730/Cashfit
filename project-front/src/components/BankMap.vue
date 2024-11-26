<template>
  <div v-if="!accountStore.isLogin" class="error-container">
    <p>로그인이 필요한 서비스입니다.</p>
  </div>

  <div v-else class="map-container">
    <div class="filter-section">
      <!-- 현재 위치 표시 및 초기화 버튼 -->
      <div class="current-location">
        <span>현재 설정된 지역: {{ accountStore.user?.user_info?.sido }} {{ accountStore.user?.user_info?.sigungus }}</span>

        <button @click="resetToUserLocation" class="reset-button" v-if="isLocationChanged">내 지역으로 돌아가기</button>
      </div>
      <v-spacer></v-spacer>
      <select v-model="sido" class="select-box" @change="onSidoChange">
        <option value="">시 / 도 선택</option>
        <option v-for="sido in sidoList">
          {{ sido }}
        </option>
      </select>

      <select v-model="sigugun" class="select-box">
        <option value="">구 / 군 선택</option>
        <option v-for="sigugun in sigugunList">
          {{ sigugun }}
        </option>
      </select>
      <button @click="searchBranches" class="search-button">검색</button>
    </div>
    <div class="content-container">
      <div ref="mapContainer" class="map-view"></div>
      <div class="place-list" v-if="places.length > 0">
        <h2>검색 결과 ({{ places.length }})</h2>
        <div v-for="(place, index) in places" :key="place.id" class="place-item" @click="focusPlace(index)"
          @mouseover="highlightMarker(index)" @mouseleave="unhighlightMarker(index)">
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

const props = defineProps({
  bank: {
    type: String,
    required: true,
  },
});

// Refs
const sido = ref("");
const sigugun = ref("");
const places = ref([]);
const activeMarkerIndex = ref(null);
const isLocationChanged = ref(false);
const mapContainer = ref(null);
const mapInstance = ref(null);
const markers = ref([]);

// Computed
const sidoList = computed(() => addressStore.address_infos.map((info) => info.sido));
const sigugunList = computed(() => {
  const selectedSido = addressStore.address_infos.find((info) => info.sido === sido.value);
  return selectedSido ? selectedSido.sigungus : [];
});

// 거리 포맷팅 함수
const formatDistance = (distance) => {
  if (distance < 1000) {
    return `${distance}m`;
  }
  return `${(distance / 1000).toFixed(1)}km`;
};

// 시도 변경 시 처리
const onSidoChange = () => {
  sigugun.value = "";
  checkLocationChanged();
};

// 위치 변경 확인
const checkLocationChanged = () => {
  isLocationChanged.value = sido.value !== accountStore.user?.user_info?.sido || sigugun.value !== accountStore.user?.user_info?.sigungus;
};

// 사용자 위치로 초기화
const resetToUserLocation = () => {
  if (!accountStore.user?.user_info) {
    console.warn("사용자 정보를 찾을 수 없습니다.");
    return;
  }

  sido.value = accountStore.user.user_info.sido;
  sigugun.value = accountStore.user.user_info.sigungus;
  isLocationChanged.value = false;
  searchBranches();
};

// 카카오맵 초기화
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
    level: 3,
  };

  mapInstance.value = new window.kakao.maps.Map(container, options);

  window.kakao.maps.event.addListener(mapInstance.value, "click", (mouseEvent) => {
    // console.log(mouseEvent.latLng);
  });
};

// 마커 관련 함수들
const focusPlace = (index) => {
  const place = places.value[index];
  const moveLatLng = new window.kakao.maps.LatLng(place.y, place.x);
  mapInstance.value.setCenter(moveLatLng);
  mapInstance.value.setLevel(3);

  if (markers.value[index]) {
    const marker = markers.value[index];
    marker.infoWindow.open(mapInstance.value, marker);
  }
};

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

// 검색 함수
const searchBranches = () => {
  if (!mapInstance.value) {
    console.error("지도가 초기화되지 않았습니다.");
    return;
  }

  if (!sido.value || !sigugun.value) {
    console.warn("지역이 선택되지 않았습니다.");
    return;
  }
  const ps = new window.kakao.maps.services.Places();
  const query = `${sido.value} ${sigugun.value} ${props.bank}`;

  checkLocationChanged();

  ps.keywordSearch(query, (data, status, pagination) => {
    if (status === window.kakao.maps.services.Status.OK) {
      markers.value.forEach((marker) => marker.setMap(null));
      markers.value = [];

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

// 컴포넌트 마운트 시 초기화
onMounted(async () => {
  try {
    // 사용자 정보가 없으면 가져오기
    if (accountStore.isLogin && !accountStore.user) {
      await accountStore.getProfile();
    }

    if (!KAKAO_API_KEY) {
      alert("Kakao API 키가 설정되지 않았습니다. .env 파일을 확인하세요.");
      return;
    }

    // user_info에서 위치 정보 가져오기
    if (accountStore.user?.user_info) {
      sido.value = accountStore.user.user_info.sido;
      sigugun.value = accountStore.user.user_info.sigungus;
      // console.log("Setting initial location:", sido.value, sigugun.value);
    }

    loadKaKaoMap(mapContainer.value);

    // 초기값이 설정된 후 검색 실행
    setTimeout(() => {
      if (sido.value && sigugun.value) {
        searchBranches();
      }
    }, 1000);
  } catch (error) {
    console.error("초기화 중 오류 발생:", error);
  }
});

// 추가로 watch를 설정하여 user 정보가 나중에 로드되었을 때도 대응
watch(
  () => accountStore.user?.user_info,
  (newUserInfo) => {
    if (newUserInfo && (!sido.value || !sigugun.value)) {
      sido.value = newUserInfo.sido;
      sigugun.value = newUserInfo.sigungus;
      if (mapInstance.value) {
        searchBranches();
      }
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
/* 스타일은 기존과 동일 */
.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  font-size: 16px;
  color: #dc3545;
}

/* 나머지 스타일은 기존 코드와 동일 */
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

.current-location {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-right: 20px;
  font-size: 14px;
  color: #666;
}

.reset-button {
  padding: 6px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.2s;
}

.reset-button:hover {
  background-color: #45a049;
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
