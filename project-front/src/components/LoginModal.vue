<template>
  <v-dialog :model-value="isOpen" @update:model-value="$emit('update:isOpen', $event)" width="400" persistent>
    <v-card class="pa-6">
      <div class="d-flex justify-space-between align-center mb-4">
        <v-card-title class="text-h5 font-weight-bold pa-0">로그인</v-card-title>
        <v-btn icon="mdi-close" variant="text" size="small" @click="$emit('update:isOpen', false)"></v-btn>
      </div>

      <v-form>
        <v-text-field v-model="email" label="이메일" prepend-inner-icon="mdi-email" variant="outlined" class="mb-4"></v-text-field>

        <v-text-field
          v-model="password"
          label="비밀번호"
          prepend-inner-icon="mdi-lock"
          :type="showPassword ? 'text' : 'password'"
          :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          variant="outlined"
          @click:append-inner="showPassword = !showPassword"
        ></v-text-field>

        <div class="d-flex align-center justify-space-between mb-6">
          <v-checkbox v-model="rememberMe" label="로그인 유지" density="compact" hide-details></v-checkbox>
          <a href="#" class="text-decoration-none text-caption">비밀번호 찾기</a>
        </div>

        <v-btn color="primary" size="large" block @click="login" class="mb-3">로그인</v-btn>

        <div class="text-center text-caption">
          계정이 없으신가요?
          <router-link to="/sign_up" class="text-decoration-none" @click="$emit('update:isOpen', false)">회원가입</router-link>
        </div>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["update:isOpen"]);

const email = ref("");
const password = ref("");
const showPassword = ref(false);
const rememberMe = ref(false);
const login = () => {
  console.log("로그인 시도", {
    email: email.value,
    password: password.value,
    rememberMe: rememberMe.value,
  });
};
// const login = () => {
//   // 로그인 로직 구현
//   // 성공 시 모달 닫기
//   // emit('update:modelValue', false)
// };
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}

.v-btn {
  text-transform: none;
  font-weight: 500;
}

a.text-decoration-none {
  color: rgb(var(--v-theme-primary));
}
</style>
