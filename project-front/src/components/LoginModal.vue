<template>
  <v-dialog :model-value="isOpen" @update:model-value="$emit('update:isOpen', $event)" width="400" persistent>
    <v-card class="pa-6">
      <div class="d-flex justify-space-between align-center mb-4">
        <v-card-title class="text-h5 font-weight-bold pa-0">로그인</v-card-title>
        <v-btn icon="mdi-close" variant="text" size="small" @click="$emit('update:isOpen', false)"></v-btn>
      </div>

      <v-form @submit.prevent="login">
        <v-text-field
          v-model="username"
          label="이메일"
          prepend-inner-icon="mdi-email"
          variant="outlined"
          class="mb-4"
          :error-messages="errors.username"
          :error="!!errors.username"
          @input="clearError('username')"
        ></v-text-field>

        <v-text-field
          v-model="password"
          label="비밀번호"
          prepend-inner-icon="mdi-lock"
          :type="showPassword ? 'text' : 'password'"
          :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          variant="outlined"
          :error-messages="errors.password"
          :error="!!errors.password"
          @input="clearError('password')"
          @click:append-inner="showPassword = !showPassword"
        ></v-text-field>

        <div class="d-flex align-center justify-space-between mb-6">
          <v-checkbox v-model="rememberMe" label="로그인 유지" density="compact" hide-details></v-checkbox>
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
import { useAccount } from "@/stores/accounts";
import { computed, ref, watch } from "vue";
import { translateErrorMessage } from "@/assets/errorMessages";

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
});

const emit = defineEmits(["update:isOpen"]);
const store = useAccount();
const username = ref("");
const password = ref("");
const showPassword = ref(false);
const rememberMe = ref(false);

// 에러 상태 관리
const errors = ref({
  username: "",
  password: "",
  non_field_errors: "", // 전체 폼 에러를 위한 필드
});

// 에러 메시지 초기화 함수
const clearError = (field) => {
  errors.value[field] = "";
};

const login = async () => {
  // 입력값 검증
  if (!username.value) {
    errors.value.username = "아이디를 입력해주세요";
    return;
  }
  if (!password.value) {
    errors.value.password = "비밀번호를 입력해주세요";
    return;
  }

  const payload = {
    username: username.value,
    password: password.value,
  };

  try {
    await store.login(payload);
    emit("update:isOpen", false);
  } catch (error) {
    if (error.response?.data) {
      if (error.response.data.non_field_errors) {
        // non_field_errors 처리 - 이를 username 필드의 에러로 표시
        const errorMessage = error.response.data.non_field_errors[0];
        if (errorMessage === "Unable to log in with provided credentials.") {
          errors.value.username = "아이디 또는 비밀번호가 일치하지 않습니다.";
        } else {
          errors.value.username = translateErrorMessage(errorMessage);
        }
      } else {
        // 다른 필드별 에러 처리
        Object.entries(error.response.data).forEach(([key, value]) => {
          if (errors.value[key] !== undefined) {
            errors.value[key] = translateErrorMessage(Array.isArray(value) ? value[0] : value);
          }
        });
      }
    }
  }
};

watch(
  () => store.isLogin,
  (newValue) => {
    if (newValue) {
      emit("update:isOpen", false);
    }
  }
);

// 모달이 닫힐 때 에러 메시지와 입력값 초기화
watch(
  () => props.isOpen,
  (newValue) => {
    if (!newValue) {
      username.value = "";
      password.value = "";
      Object.keys(errors.value).forEach((key) => {
        errors.value[key] = "";
      });
    }
  }
);
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
