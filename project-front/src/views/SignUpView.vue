<template>
  <v-container class="fill-height bg-grey-lighten-4">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="5">
        <v-card class="signup-card mx-auto rounded-lg" elevation="3">
          <div class="text-center pt-8 pb-4">
            <v-avatar color="primary" size="52" class="mb-4">
              <v-icon size="32" color="white">mdi-account-plus</v-icon>
            </v-avatar>
            <h2 class="text-h4 font-weight-medium mb-1">회원가입</h2>
            <p class="text-body-1 text-medium-emphasis">새로운 계정을 만들어보세요</p>
          </div>

          <v-card-text>
            <v-form @submit.prevent="handleSubmit" v-model="isValid" class="px-2">
              <v-text-field
                v-model="email"
                label="이메일"
                :rules="emailRules"
                required
                prepend-inner-icon="mdi-email"
                variant="outlined"
                density="comfortable"
                bg-color="grey-lighten-5"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="비밀번호"
                :rules="passwordRules"
                required
                :type="showPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                density="comfortable"
                bg-color="grey-lighten-5"
                class="mb-4"
                hint="8자 이상, 대소문자, 숫자 포함"
                persistent-hint
              ></v-text-field>

              <v-text-field
                v-model="passwordConfirm"
                label="비밀번호 확인"
                :rules="passwordConfirmRules"
                required
                :type="showPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock-check"
                variant="outlined"
                density="comfortable"
                bg-color="grey-lighten-5"
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="name"
                label="이름"
                :rules="nameRules"
                required
                prepend-inner-icon="mdi-account"
                variant="outlined"
                density="comfortable"
                bg-color="grey-lighten-5"
                class="mb-6"
              ></v-text-field>

              <v-btn color="primary" block size="large" type="submit" :disabled="!isValid" class="mb-4 text-subtitle-1" :loading="isSubmitting" elevation="2">
                가입하기
                <v-icon end icon="mdi-arrow-right" class="ml-1"></v-icon>
              </v-btn>

              <v-divider class="mb-4"><span class="text-medium-emphasis">또는</span></v-divider>

              <v-btn color="secondary" block size="large" variant="tonal" @click="showLoginModal = true" class="mb-4">
                <v-icon start icon="mdi-login" class="mr-1"></v-icon>
                로그인하기
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <p class="text-center mt-4 text-medium-emphasis">
          가입하면
          <a href="#" class="text-primary">이용약관</a>
          과
          <a href="#" class="text-primary">개인정보 처리방침</a>
          에 동의하게 됩니다.
        </p>
      </v-col>
    </v-row>
  </v-container>

  <LoginModal :is-open="showLoginModal" @update:is-open="showLoginModal = $event" />
</template>

<script setup>
import { ref, computed } from "vue";
import LoginModal from "@/components/LoginModal.vue";

const showLoginModal = ref(false);
const email = ref("");
const password = ref("");
const passwordConfirm = ref("");
const name = ref("");
const showPassword = ref(false);
const isSubmitting = ref(false);

const emailRules = [(v) => !!v || "이메일을 입력해주세요", (v) => /.+@.+\..+/.test(v) || "올바른 이메일 형식이 아닙니다"];

const passwordRules = [
  (v) => !!v || "비밀번호를 입력해주세요",
  (v) => v.length >= 8 || "비밀번호는 최소 8자 이상이어야 합니다",
  (v) => (/[A-Z]/.test(v) && /[a-z]/.test(v) && /[0-9]/.test(v)) || "대문자, 소문자, 숫자를 모두 포함해야 합니다",
];

const passwordConfirmRules = [(v) => !!v || "비밀번호를 한번 더 입력해주세요", (v) => v === password.value || "비밀번호가 일치하지 않습니다"];

const nameRules = [(v) => !!v || "이름을 입력해주세요", (v) => v.length >= 2 || "이름은 최소 2자 이상이어야 합니다"];

const isValid = computed(() => {
  const allRulesValid = [
    ...emailRules.map((rule) => rule(email.value)),
    ...passwordRules.map((rule) => rule(password.value)),
    ...passwordConfirmRules.map((rule) => rule(passwordConfirm.value)),
    ...nameRules.map((rule) => rule(name.value)),
  ];
  return allRulesValid.every((result) => result === true);
});

async function handleSubmit() {
  if (isValid.value) {
    isSubmitting.value = true;
    try {
      // API 호출 또는 회원가입 로직 구현
      await new Promise((resolve) => setTimeout(resolve, 1000)); // 시뮬레이션된 API 호출
      console.log("Form submitted:", {
        email: email.value,
        password: password.value,
        name: name.value,
      });
    } catch (error) {
      console.error("회원가입 중 오류가 발생했습니다:", error);
    } finally {
      isSubmitting.value = false;
    }
  }
}
</script>

<style scoped>
.signup-card {
  max-width: 480px;
}

:deep(.v-field) {
  border-radius: 8px;
}

:deep(.v-field__outline) {
  border-width: 1px;
}

:deep(.v-field--focused .v-field__outline) {
  border-width: 2px;
}

:deep(.v-divider) {
  position: relative;
  margin: 24px 0;
}

:deep(.v-divider span) {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 0 16px;
  font-size: 14px;
}
</style>
