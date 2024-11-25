<template>
  <v-main style="margin-top: 40px" class="fill-height custom-bg">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="signup-card">
          <!-- 헤더 섹션 -->
          <div class="card-header pa-8 text-center">
            <v-avatar class="mb-4" color="primary" size="56">
              <v-icon icon="mdi-account-plus" size="24" color="white" />
            </v-avatar>
            <h2 class="text-h4 font-weight-bold mb-2 gradient-text">회원가입</h2>
            <p class="text-subtitle-1 text-medium-emphasis">회원이 되어 다양한 혜택을 경험해 보세요!</p>
          </div>

          <v-divider></v-divider>

          <!-- 폼 섹션 -->
          <div class="pa-8">
            <v-form @submit.prevent="handleSignup">
              <!-- 계정 정보 섹션 -->
              <div class="form-section mb-6">
                <div class="text-subtitle-1 font-weight-bold mb-4">계정 정보</div>
                <v-text-field
                  v-model="username"
                  label="아이디 입력 (6~20자)"
                  variant="outlined"
                  density="comfortable"
                  class="custom-field mb-3"
                  :error-messages="errors.username"
                  :error="!!errors.username"
                  @input="handleUsernameInput"
                  prepend-inner-icon="mdi-account"
                />

                <v-text-field
                  v-model="password1"
                  label="비밀번호 입력 (8~20자)"
                  type="password"
                  variant="outlined"
                  density="comfortable"
                  class="custom-field mb-3"
                  :error-messages="errors.password1"
                  :error="!!errors.password1"
                  @input="handlePassword1Input"
                  prepend-inner-icon="mdi-lock"
                />

                <v-text-field
                  v-model="password2"
                  label="비밀번호 확인"
                  type="password"
                  variant="outlined"
                  density="comfortable"
                  class="custom-field mb-3"
                  :error-messages="errors.password2"
                  :error="!!errors.password2"
                  @input="handlePassword2Input"
                  prepend-inner-icon="mdi-lock-check"
                />
              </div>

              <!-- 개인 정보 섹션 -->
              <div class="form-section mb-6">
                <div class="text-subtitle-1 font-weight-bold mb-4">개인 정보</div>
                <v-text-field
                  v-model="nickname"
                  label="닉네임 입력"
                  variant="outlined"
                  density="comfortable"
                  class="custom-field mb-3"
                  :error-messages="errors.nickname"
                  :error="!!errors.nickname"
                  @input="handleNicknameInput"
                  prepend-inner-icon="mdi-account-circle"
                />

                <v-text-field
                  v-model="age"
                  label="나이 입력 (숫자만)"
                  variant="outlined"
                  density="comfortable"
                  class="custom-field mb-3"
                  :error-messages="errors.age"
                  :error="!!errors.age"
                  @input="handleAgeInput"
                  prepend-inner-icon="mdi-calendar"
                />

                <v-text-field
                  v-model="capital"
                  label="자본금 입력 (숫자만)"
                  variant="outlined"
                  density="comfortable"
                  class="custom-field mb-3"
                  suffix="만원"
                  :error-messages="errors.capital"
                  :error="!!errors.capital"
                  @input="handleCapitalInput"
                  prepend-inner-icon="mdi-currency-usd"
                />
              </div>

              <!-- 주소 정보 섹션 -->
              <div class="form-section mb-6">
                <div class="text-subtitle-1 font-weight-bold mb-4">주소 정보</div>
                <v-select
                  v-model="sido"
                  :items="sidoList"
                  label="시/도 선택"
                  variant="outlined"
                  density="comfortable"
                  class="custom-field mb-3"
                  :error-messages="errors.sido"
                  :error="!!errors.sido"
                  @change="onSidoChange"
                  prepend-inner-icon="mdi-map-marker"
                />

                <v-select
                  v-model="sigugun"
                  :items="sigugunList"
                  label="시/군/구 선택"
                  variant="outlined"
                  density="comfortable"
                  class="custom-field mb-6"
                  :error-messages="errors.sigugun"
                  :error="!!errors.sigugun"
                  :disabled="!sigugunList.length"
                  prepend-inner-icon="mdi-map-marker-radius"
                />
              </div>

              <!-- 버튼 그룹 -->
              <div class="d-flex gap-3">
                <v-btn color="primary" block type="submit" :loading="isSubmitting" class="action-btn" height="48" elevation="0">가입하기</v-btn>
                <v-btn block @click="showLoginModal = true" class="action-btn" color="grey-lighten-3" height="48" elevation="0">취소</v-btn>
              </div>
            </v-form>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-main>
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
    await swal({
      title: "회원가입 성공!",
      text: "더 많은 경험을 체험해보세요!!",
      icon: "success",
      button: "확인",
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

<style scoped>
.custom-bg {
  background: linear-gradient(135deg, #f6f7f9 0%, #edf2f7 100%);
  min-height: 100vh;
}

.signup-card {
  border-radius: 24px;
  background: white;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08) !important;
  overflow: hidden;
}

.card-header {
  background: linear-gradient(to right, #ffffff, #f8f9fa);
}

.gradient-text {
  background: linear-gradient(45deg, #1a237e, #0d47a1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.custom-field {
  :deep(.v-field) {
    border-radius: 12px;
    transition: all 0.3s ease;
  }

  :deep(.v-field:hover) {
    border-color: #1a237e;
  }

  :deep(.v-field--focused) {
    border-color: #1a237e;
    box-shadow: 0 0 0 4px rgba(26, 35, 126, 0.1);
  }

  :deep(.v-field__input) {
    padding: 16px;
    font-size: 1rem;
  }

  :deep(.v-label) {
    font-size: 0.95rem;
    color: #64748b;
  }
}

.form-section {
  background: #f8fafc;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
}

.action-btn {
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: none;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.action-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 입력 필드 아이콘 스타일 */
:deep(.v-input__prepend) {
  margin-right: 8px;
  color: #64748b;
}

/* 취소 버튼 hover 효과 */
.action-btn.v-btn--variant-flat {
  background: #f1f5f9;
  color: #64748b;
}

.action-btn.v-btn--variant-flat:hover {
  background: #e2e8f0;
  color: #1e293b;
}
</style>
