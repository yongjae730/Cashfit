<template>
  <div class="link-card" @click="$emit('click')">
    <div class="card-content">
      <div class="icon-section">
        <v-icon icon="mdi-currency-usd" size="48" color="primary"></v-icon>
      </div>
      <div class="text-section">
        <h3 class="text-h5 font-weight-bold mb-2">실시간 환율 정보</h3>
        <p class="text-subtitle-1 text-medium-emphasis">전 세계 주요 통화의 실시간 환율 정보를 확인하세요</p>
      </div>
    </div>
    <div class="action-section">
      <v-btn variant="text" color="primary" append-icon="mdi-arrow-right">환율 정보 보기</v-btn>
    </div>
  </div>
</template>

<style scoped>
.link-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.link-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
}

.card-content {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 24px;
}

.icon-section {
  background: rgba(var(--v-theme-primary), 0.1);
  padding: 20px;
  border-radius: 16px;
}

.action-section {
  padding-top: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}
</style>
