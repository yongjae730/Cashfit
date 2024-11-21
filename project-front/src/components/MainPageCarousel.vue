<template>
  <div class="main-carousel-section">
    <v-row>
      <v-col cols="12">
        <v-carousel hide-delimiters cycle show-arrows="hover" height="400px">
          <v-carousel-item v-for="(slide, i) in slides" :key="i">
            <div class="d-flex flex-column align-center justify-center" style="height: 100%">
              <h1 class="v-typography display-large primary--text">{{ slide.title }}</h1>
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
  padding-top: 20px;
  padding-bottom: 20px;
}
</style>
