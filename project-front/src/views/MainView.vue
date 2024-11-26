<template>
  <v-main class="modern-main">
    <!-- 히어로 섹션 -->
    <div class="hero-section">
      <MainPageCarousel v-if="carouselSlides.length > 0" :slides="carouselSlides" />
      <div class="hero-overlay"></div>
    </div>

    <!-- 네비게이션 -->
    <div class="nav-section">
      <MiddleNav class="floating-nav" />
    </div>

    <!-- 기능 소개 섹션 -->
    <section class="features-section">
      <v-container>
        <h2 class="section-title">CashFit의 주요 기능을 만나보세요!</h2>
        <p class="section-subtitle">당신의 더 나은 금융 생활을 위한 모든 기능</p>

        <div class="feature-grid">
          <div class="feature-card">
            <div class="icon-wrapper">
              <v-icon icon="mdi-chart-box" size="48" color="primary"></v-icon>
            </div>
            <h3>금리가 높은 상품</h3>
            <p>현재 기간별 가장 금리가 높은 상품</p>
            <v-btn color="primary" class="mt-4" @click="showFeature('products')" :class="{ 'active-feature': activeFeature === 'products' }">살펴보기</v-btn>
          </div>
          <div class="feature-card">
            <div class="icon-wrapper">
              <v-icon icon="mdi-map-marker-radius" size="48" color="primary"></v-icon>
            </div>
            <h3>스마트한 지점 찾기</h3>
            <p>내 주변 가까운 은행 한눈에 확인</p>
            <v-btn color="primary" class="mt-4" @click="showFeature('map')" :class="{ 'active-feature': activeFeature === 'map' }">살펴보기</v-btn>
          </div>
          <div class="feature-card">
            <div class="icon-wrapper">
              <v-icon icon="mdi-bank" size="48" color="primary"></v-icon>
            </div>
            <h3>CahsFit은?</h3>
            <p>이런 회사예요</p>
            <v-btn color="primary" class="mt-4" @click="showFeature('info')" :class="{ 'active-feature': activeFeature === 'info' }">살펴보기</v-btn>
          </div>
        </div>
      </v-container>
    </section>
    <v-expand-transition>
      <section v-if="activeFeature" class="demo-section">
        <v-container>
          <div class="demo-header">
            <h3>{{ getFeatureTitle }}</h3>
            <v-btn icon="mdi-close" variant="text" @click="closeFeature"></v-btn>
          </div>
          <!-- 기능별 컴포넌트 표시 -->
          <div class="demo-content">
            <MainProductList v-if="activeFeature === 'products'" />
            <MainPageBank v-if="activeFeature === 'map'" />
            <div v-if="activeFeature === 'info'" class="company-info">
              <!-- 미션 섹션 -->
              <div class="mission-section">
                <v-icon :icon="companyInfo.mission.icon" size="48" color="primary" class="mb-4" />
                <h3 class="text-h4 font-weight-bold mb-2">{{ companyInfo.mission.title }}</h3>
                <p class="text-body-1">{{ companyInfo.mission.content }}</p>
              </div>

              <!-- 통계 섹션 -->
              <div class="stats-section">
                <div v-for="(stat, index) in companyInfo.stats" :key="index" class="stat-item">
                  <div class="stat-number">{{ stat.number }}</div>
                  <div class="stat-label">{{ stat.label }}</div>
                </div>
              </div>

              <!-- 가치 섹션 -->
              <div class="values-section">
                <div v-for="(value, index) in companyInfo.values" :key="index" class="value-card">
                  <v-icon :icon="value.icon" size="32" color="primary" class="mb-3" />
                  <h4 class="text-h6 font-weight-bold mb-2">{{ value.title }}</h4>
                  <p class="text-body-2">{{ value.content }}</p>
                </div>
              </div>
            </div>
          </div>
        </v-container>
      </section>
    </v-expand-transition>

    <!-- 환율 섹션 -->
    <section class="features-section bg-gradient-light">
      <v-container>
        <h2 class="section-title">빠르고 정확한 환율 정보</h2>
        <p class="section-subtitle">실시간으로 업데이트되는 전 세계 환율을 확인하세요</p>

        <div class="feature-grid single-feature">
          <div class="feature-card wide-card">
            <div class="icon-wrapper">
              <v-icon icon="mdi-currency-usd" size="48" color="primary"></v-icon>
            </div>
            <!-- <v-img src="/bank_images/환율정보.png" height="300" class="feature-image" cover /> -->
            <h3>실시간 환율 정보</h3>
            <p>
              전 세계 주요 통화의 실시간 환율 정보를 간편하게 확인하고
              <br />
              계산해보세요
            </p>
            <v-btn color="primary" class="mt-4" @click="router.push({ name: 'exchange' })" size="large">환율 확인하러 가기</v-btn>
          </div>
        </div>
      </v-container>
    </section>

    <!-- 가상화폐 섹션 -->
    <section class="features-section bg-gradient-dark">
      <v-container>
        <h2 class="section-title text-white">실시간 가상화폐 시세</h2>
        <p class="section-subtitle text-grey-lighten-3">비트코인부터 알트코인까지 한눈에 확인하세요</p>

        <div class="feature-grid single-feature">
          <div class="feature-card dark-card">
            <div class="icon-wrapper dark">
              <v-icon icon="mdi-bitcoin" size="48" color="warning"></v-icon>
            </div>
            <!-- <v-img src="/bank_images/가상화폐.png" height="300" class="feature-image" cover /> -->
            <h3 class="text-white">가상화폐 실시간 시세</h3>
            <p class="text-grey-lighten-3">
              실시간 시세와 차트를 통해
              <br />
              가상화폐 시장을 분석해보세요
            </p>
            <v-btn color="warning" class="mt-4" @click="router.push({ name: 'Crypto' })" size="large">시세 확인하러 가기</v-btn>
          </div>
        </div>
      </v-container>
    </section>
    <!-- 기능 체험 영역 -->
  </v-main>
</template>

<script setup>
import MainPageCarousel from "@/components/MainPageCarousel.vue";
import MainProductList from "@/components/MainProductList.vue";
import MainPageBank from "@/components/MainPageBank.vue";
import { ref, onMounted, computed } from "vue";
import MiddleNav from "@/components/MiddleNav.vue";
import router from "@/router";

// 캐러셀 데이터
const carouselSlides = ref([]);
// 활성화된 기능 상태 관리
const activeFeature = ref(null);

// 기능 타이틀 계산
const getFeatureTitle = computed(() => {
  switch (activeFeature.value) {
    case "rates":
      return "실시간 금리 비교";
    case "products":
      return "맞춤형 상품 추천";
    case "map":
      return "스마트한 지점 찾기";
    default:
      return "";
  }
});

const companyInfo = {
  mission: {
    title: "우리의 미션",
    content: "모든 사람이 쉽고 현명한 금융 생활을 할 수 있도록 돕습니다.",
    icon: "mdi-lighthouse",
  },
  values: [
    {
      title: "투명성",
      content: "모든 금융 정보를 투명하게 제공합니다.",
      icon: "mdi-shield-check",
    },
    {
      title: "혁신",
      content: "AI 기술로 새로운 금융 경험을 만듭니다.",
      icon: "mdi-lightbulb",
    },
    {
      title: "신뢰성",
      content: "정확한 데이터로 신뢰할 수 있는 정보를 제공합니다.",
      icon: "mdi-handshake",
    },
  ],
  stats: [
    {
      number: "50만+",
      label: "월간 사용자 였으면 좋겠다..",
    },
    {
      number: "1,000+",
      label: "제휴 지점 됐으면 좋겠다..",
    },
    {
      number: "98%",
      label: "사용자 만족도면 좋겠다..",
    },
  ],
};

const fetchCarouselSlides = async () => {
  return [
    {
      image: `carousel/carousel1.png`,
      title: "금융 상품 추천",
      subtitle: "당신을 위한 맞춤 금융 상품",
    },
    {
      image: `carousel/carousel2.png`,
      title: "해외 여행을 준비중이라면",
      subtitle: "실시간 환율 조회",
    },
    {
      image: `carousel/carousel3.png`,
      title: "도파민이 필요하다면",
      subtitle: "암호 화폐",
    },
  ];
};

// 기능 표시/숨김 메소드
const showFeature = (feature) => {
  if (activeFeature.value === feature) {
    activeFeature.value = null;
  } else {
    activeFeature.value = feature;
    // 해당 섹션으로 부드럽게 스크롤
    const demoSection = document.querySelector(".demo-section");
    if (demoSection) {
      demoSection.scrollIntoView({ behavior: "smooth" });
    }
  }
};

const closeFeature = () => {
  activeFeature.value = null;
};

onMounted(async () => {
  carouselSlides.value = await fetchCarouselSlides();
});
</script>

<style scoped>
.modern-main {
  background: linear-gradient(135deg, #f6f9fc 0%, #edf2f7 100%);
  overflow-x: hidden;
}

.hero-section {
  position: relative;
  width: 100%;
  margin-bottom: -60px;
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: linear-gradient(to bottom, transparent, #f6f9fc);
  z-index: 1;
}

.nav-section {
  position: relative;
  z-index: 2;
  margin: 0 auto;
  max-width: 1200px;
  padding: 0 16px;
}

.floating-nav {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.features-section {
  padding: 80px 0;
  text-align: center;
  background: linear-gradient(135deg, #f6f9fc 0%, #edf2f7 100%);
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1f36;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 1.25rem;
  color: #4f566b;
  margin-bottom: 64px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  border-radius: 24px;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
}

.feature-image {
  border-radius: 16px;
  margin-bottom: 24px;
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a1f36;
  margin-bottom: 8px;
}

.feature-card p {
  color: #4f566b;
  font-size: 1.1rem;
}

.feature-card .v-btn {
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
}

.feature-card:hover .v-btn {
  opacity: 1;
  transform: translateY(0);
}

.active-feature {
  background-color: #1a73e8 !important;
  color: white !important;
}

.demo-section {
  background: white;
  padding: 40px 0;
  margin-top: -40px;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.05);
}

.demo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 16px;
}

.demo-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a1f36;
}

.demo-content {
  display: flex;
  justify-content: center;
  min-height: 400px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 960px) {
  .feature-grid {
    grid-template-columns: 1fr;
    padding: 0 16px;
  }

  .feature-card .v-btn {
    opacity: 1;
    transform: translateY(0);
  }

  .section-title {
    font-size: 2rem;
  }
}
.company-info {
  padding: 40px 0;
}

.mission-section {
  text-align: center;
  max-width: 700px;
  margin: 0 auto 60px;
  padding: 40px;
  background: linear-gradient(145deg, #ffffff, #f8fafc);
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 900px;
  margin: 0 auto 60px;
  padding: 20px;
}

.stat-item {
  text-align: center;
  padding: 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a73e8;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 1.1rem;
  color: #4f566b;
}

.values-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.value-card {
  text-align: center;
  padding: 32px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.value-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

@media (max-width: 960px) {
  .stats-section,
  .values-section {
    grid-template-columns: 1fr;
    padding: 20px;
  }

  .mission-section {
    margin: 20px;
    padding: 20px;
  }

  .stat-number {
    font-size: 2rem;
  }
}
.icon-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: -40px auto 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  z-index: 1;
  backdrop-filter: blur(10px);
}

.feature-card {
  position: relative;
  overflow: hidden;
  padding-top: 40px; /* 아이콘을 위한 상단 여백 추가 */
}

.feature-card:hover .icon-wrapper {
  transform: scale(1.1);
  transition: transform 0.3s ease;
}
.bg-gradient-light {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.bg-gradient-dark {
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
  margin-top: -40px; /* 섹션 간 자연스러운 연결을 위해 */
  padding-top: 80px;
}

.single-feature {
  grid-template-columns: 1fr !important;
  max-width: 900px !important;
}

.wide-card {
  padding: 40px;
  text-align: center;
}

.dark-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-card:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.icon-wrapper.dark {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
}

.feature-image {
  border-radius: 20px;
  margin: 30px 0;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

/* 반응형 디자인 */
@media (max-width: 960px) {
  .single-feature {
    padding: 0 16px;
  }

  .wide-card {
    padding: 20px;
  }

  .feature-card h3 {
    font-size: 1.3rem;
  }

  .feature-card p {
    font-size: 1rem;
  }

  .bg-gradient-dark {
    margin-top: 0;
  }
}

/* 호버 효과 */
.feature-card:hover .feature-image {
  transform: scale(1.03);
  transition: transform 0.3s ease;
}

.feature-card .v-btn {
  transition: all 0.3s ease;
}

.feature-card:hover .v-btn {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
</style>
