<template>
  <v-container class="fill-height" style="background-color: #f0f4f8">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="pa-6" style="border-radius: 16px; box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.1); background-color: white">
          <h2 class="text-center font-weight-bold mb-2" style="font-size: 24px; color: #333">회원가입</h2>
          <p class="text-center mb-6" style="color: #777">회원이 되어 다양한 혜택을 경험해 보세요!</p>

          <v-form @submit.prevent="handleSignup">
            <v-text-field
              v-model="username"
              label="아이디 입력 (6~20자)"
              outlined
              dense
              class="mb-4"
              :error-messages="errors.username"
              :error="!!errors.username"
              @input="handleUsernameInput"
              style="border-radius: 8px; border-color: red !important"
            />

            <v-text-field
              v-model="password1"
              label="비밀번호 입력 (8~20자)"
              type="password"
              outlined
              dense
              class="mb-4"
              :error-messages="errors.password1"
              :error="!!errors.password1"
              @input="handlePassword1Input"
              style="border-radius: 8px"
            />

            <v-text-field
              v-model="password2"
              label="비밀번호 확인"
              type="password"
              outlined
              dense
              class="mb-4"
              :error-messages="errors.password2"
              :error="!!errors.password2"
              @input="handlePassword2Input"
              style="border-radius: 8px"
            />

            <v-text-field
              v-model="nickname"
              label="닉네임 입력"
              outlined
              dense
              class="mb-4"
              :error-messages="errors.nickname"
              :error="!!errors.nickname"
              @input="handleNicknameInput"
              style="border-radius: 8px"
            />

            <v-text-field
              v-model="age"
              label="나이 입력 (숫자만)"
              outlined
              dense
              class="mb-4"
              :error-messages="errors.age"
              :error="!!errors.age"
              @input="handleAgeInput"
              oninput="javascript: this.value = this.value.replace(/\D/g, '')"
              style="border-radius: 8px"
            />

            <v-text-field
              v-model="capital"
              label="자본금 입력 (숫자만)"
              outlined
              dense
              class="mb-4"
              suffix="만원"
              :error-messages="errors.capital"
              :error="!!errors.capital"
              @input="handleCapitalInput"
              oninput="javascript: this.value = this.value.replace(/\D/g, '')"
              style="border-radius: 8px"
            />

            <v-select
              v-model="sido"
              :items="sidoList"
              label="시/도 선택"
              outlined
              dense
              class="mb-4"
              :error-messages="errors.sido"
              :error="!!errors.sido"
              style="border-radius: 8px"
              @change="onSidoChange"
            />

            <v-select
              v-model="sigugun"
              :items="sigugunList"
              label="시/군/구 선택"
              outlined
              dense
              class="mb-6"
              :error-messages="errors.sigugun"
              :error="!!errors.sigugun"
              :disabled="!sigugunList.length"
              style="border-radius: 8px"
            />

            <v-btn color="primary" block type="submit" :loading="isSubmitting" class="py-3 font-weight-bold" style="border-radius: 8px; background-color: #1e88e5; color: white; font-size: 16px">
              가입하기
            </v-btn>

            <v-btn block color="secondary" @click="showLoginModal = true" class="py-3 font-weight-bold mt-3" style="border-radius: 8px; background-color: #26a69a; color: white; font-size: 16px">
              가입취소
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, ref } from "vue";
import { useAccount } from "@/stores/accounts";
import { useAddressStore } from "@/stores/address";
import { translateErrorMessage } from "@/assets/errorMessages";

const { signUp } = useAccount();
const addressStore = useAddressStore();

// Form fields
const username = ref("");
const password1 = ref("");
const password2 = ref("");
const nickname = ref("");
const age = ref("");
const capital = ref("");
const sido = ref("");
const sigugun = ref("");
const isValid = ref(false);
const isSubmitting = ref(false);

// Error states
const errors = ref({
  username: "",
  password1: "",
  password2: "",
  nickname: "",
  age: "",
  capital: "",
  sido: "",
  sigugun: "",
});

// Validation rules
const usernameRules = [
  (v) => !!v || "아이디를 입력해주세요",
  (v) => v.length >= 6 || "아이디는 최소 6자 이상이어야 합니다",
  (v) => v.length <= 20 || "아이디는 최대 20자까지 가능합니다",
  (v) => /^[a-zA-Z0-9]+$/.test(v) || "아이디는 영문자와 숫자만 사용 가능합니다",
];

const passwordRules = [
  (v) => !!v || "비밀번호를 입력해주세요",
  (v) => v.length >= 8 || "비밀번호는 최소 8자 이상이어야 합니다",
  (v) => v.length <= 20 || "비밀번호는 최대 20자까지 가능합니다",
  (v) => /[!@#$%^&*(),.?":{}|<>]/.test(v) || "비밀번호는 특수문자를 하나 이상 포함해야 합니다",
];

const passwordConfirmRules = [(v) => !!v || "비밀번호 확인을 입력해주세요", (v) => v === password1.value || "비밀번호가 일치하지 않습니다"];

const nicknameRules = [(v) => !!v || "닉네임을 입력해주세요", (v) => v.length <= 20 || "닉네임은 최대 20자까지 가능합니다"];

const ageRules = [(v) => !!v || "나이를 입력해주세요", (v) => Number(v) >= 14 || "14세 이상만 가입 가능합니다", (v) => Number(v) <= 120 || "올바른 나이를 입력해주세요"];

const capitalRules = [(v) => !!v || "자본금을 입력해주세요", (v) => Number(v) >= 0 || "0 이상의 숫자를 입력해주세요"];

// Computed properties for address
const sidoList = computed(() => addressStore.address_infos.map((info) => info.sido));
const sigugunList = computed(() => {
  const selectedSido = addressStore.address_infos.find((info) => info.sido === sido.value);
  return selectedSido ? selectedSido.sigungus : [];
});

// Methods
const validateField = (field, value, rules) => {
  for (const rule of rules) {
    const result = rule(value);
    if (result !== true) {
      errors.value[field] = result;
      return false;
    }
  }
  errors.value[field] = "";
  return true;
};

const onSidoChange = () => {
  sigugun.value = null;
  errors.value.sigugun = "";
};

// Real-time validation handlers
const handleUsernameInput = () => validateField("username", username.value, usernameRules);
const handlePassword1Input = () => {
  validateField("password1", password1.value, passwordRules);
  if (password2.value) handlePassword2Input();
};
const handlePassword2Input = () => validateField("password2", password2.value, passwordConfirmRules);
const handleNicknameInput = () => validateField("nickname", nickname.value, nicknameRules);
const handleAgeInput = () => validateField("age", age.value, ageRules);
const handleCapitalInput = () => validateField("capital", capital.value, capitalRules);

const handleSignup = async () => {
  // Validate all fields before submission
  const isUsernameValid = validateField("username", username.value, usernameRules);
  const isPassword1Valid = validateField("password1", password1.value, passwordRules);
  const isPassword2Valid = validateField("password2", password2.value, passwordConfirmRules);
  const isNicknameValid = validateField("nickname", nickname.value, nicknameRules);
  const isAgeValid = validateField("age", age.value, ageRules);
  const isCapitalValid = validateField("capital", capital.value, capitalRules);
  const isSidoValid = !!sido.value;
  const isSigugunValid = !!sigugun.value;

  if (!isSidoValid) errors.value.sido = "시/도를 선택해주세요";
  if (!isSigugunValid) errors.value.sigugun = "시/군/구를 선택해주세요";

  if (!(isUsernameValid && isPassword1Valid && isPassword2Valid && isNicknameValid && isAgeValid && isCapitalValid && isSidoValid && isSigugunValid)) {
    await swal({
      title: "입력 오류",
      text: "모든 필드를 올바르게 입력해주세요",
      icon: "error",
      button: "확인",
    });
    return;
  }

  isSubmitting.value = true;
  try {
    await signUp({
      username: username.value,
      password1: password1.value,
      password2: password2.value,
      nickname: nickname.value,
      age: age.value,
      capital: capital.value,
      sido: sido.value,
      sigungus: sigugun.value,
    });
  } catch (error) {
    if (error.response?.data) {
      // 서버에서 받은 에러 메시지 처리
      Object.entries(error.response.data).forEach(([key, value]) => {
        if (errors.value[key] !== undefined) {
          errors.value[key] = translateErrorMessage(Array.isArray(value) ? value[0] : value);
        }
      });
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>
