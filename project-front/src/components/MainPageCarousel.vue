<template>
  <div class="main-carousel-section">
    <v-row>
      <v-col cols="12">
        <v-carousel hide-delimiters cycle show-arrows="hover" height="500px">
          <v-carousel-item v-for="(slide, i) in slides" :key="i">
            <v-img :src="slide.image" class="carousel-image" cover></v-img>
            <div class="carousel-title d-flex flex-column align-center justify-center carousel-overlay" style="height: 100%">
              <h1 class="carousel-subtitle v-typography display-large primary--text">{{ slide.title }}</h1>
              <h3>{{ slide.subtitle }}</h3>
            </div>
          </v-carousel-item>
        </v-carousel>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
const props = defineProps({
  slides: {
    type: Array,
    required: true,
  },
});
</script>

<style scoped>
.main-carousel-section {
  background-color: #f3f4f6;
}
/* 텍스트 오버레이 */
.carousel-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
  text-align: center;
  color: white;
  background: rgba(0, 0, 0, 0.4); /* 어두운 오버레이 */
  padding: 20px;
}

.carousel-title {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 10px;
}

.carousel-subtitle {
  font-size: 18px;
  margin: 0;
}
</style>
