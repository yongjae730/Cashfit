<template>
  <v-footer class="footer-container" color="white" padless>
    <v-container>
      <v-row class="py-8">
        <!-- 깃허브 섹션 -->
        <v-col class="text-center" cols="12" md="4">
          <div class="mb-4">
            <h2 class="footer-title">깃허브</h2>
            <div class="title-underline"></div>
          </div>
          <div class="footer-content">
            <v-btn href="https://github.com/" target="_blank" variant="text" class="footer-link mb-2 px-4" prepend-icon="mdi-github" rounded>바로가기</v-btn>
          </div>
        </v-col>

        <!-- SSAFY 섹션 -->
        <v-col class="text-center" cols="12" md="4">
          <div class="mb-4">
            <h2 class="footer-title">SSAFY</h2>
            <div class="title-underline"></div>
          </div>
          <div class="footer-content">
            <div class="footer-item">
              <v-icon icon="mdi-palette" color="primary" class="mb-1" />
              <div class="text-body-1">디자인하고!</div>
            </div>
            <div class="footer-item">
              <v-icon icon="mdi-layers" color="primary" class="mb-1" />
              <div class="text-body-1">지식쌓고!</div>
            </div>
            <div class="footer-item">
              <v-icon icon="mdi-code-tags" color="primary" class="mb-1" />
              <div class="text-body-1">즐겁다!</div>
            </div>
          </div>
        </v-col>

        <!-- 주소 섹션 -->
        <v-col class="text-center" cols="12" md="4">
          <div class="mb-4">
            <h2 class="footer-title">주소</h2>
            <div class="title-underline"></div>
          </div>
          <div class="footer-content">
            <v-list density="compact" nav class="footer-list">
              <v-list-item v-for="(item, i) in addressItems" :key="i" :title="item" class="footer-list-item" rounded="lg">
                <template v-slot:prepend>
                  <v-icon :icon="addressIcons[i]" color="grey-darken-1" size="small"></v-icon>
                </template>
              </v-list-item>
            </v-list>
          </div>
        </v-col>
      </v-row>

      <!-- 저작권 표시 -->
      <v-divider class="my-4"></v-divider>
      <div class="text-center text-grey-darken-1 pb-4 text-body-2">© {{ new Date().getFullYear() }} CASHFIT. All rights reserved.</div>
    </v-container>
  </v-footer>
</template>

<script setup>
const addressItems = ["Blog", "Best practices", "Colors", "Color wheel", "Support"];
const addressIcons = ["mdi-post", "mdi-star", "mdi-palette", "mdi-sync", "mdi-help-circle"];
</script>

<style lang="scss" scoped>
.footer-container {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.footer-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a237e;
  margin-bottom: 0.5rem;
  position: relative;
  display: inline-block;
}

.title-underline {
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #1a237e, #90caf9);
  margin: 0 auto;
  border-radius: 2px;
}

.footer-content {
  margin-top: 1.5rem;
}

.footer-item {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #616161;
  transition: color 0.2s ease;

  &:hover {
    color: #1a237e;
  }
}

.footer-link {
  text-decoration: none;
  color: #616161;
  transition: all 0.2s ease;
  font-weight: 500;

  &:hover {
    color: #1a237e;
    transform: translateY(-2px);
  }
}

.footer-list {
  background-color: transparent;
  max-width: 200px;
  margin: 0 auto;
}

.footer-list-item {
  transition: all 0.2s ease;
  margin-bottom: 4px;

  &:hover {
    background-color: rgba(26, 35, 126, 0.05);
    transform: translateX(4px);

    :deep(.v-list-item__content) {
      color: #1a237e;
    }

    :deep(.v-icon) {
      color: #1a237e !important;
    }
  }
}

:deep(.v-list-item-title) {
  font-size: 0.9rem !important;
  color: #616161;
}
</style>
