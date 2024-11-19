<template>
  <v-container class="fill-height" style="background-color: #f0f4f8">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="pa-6" style="border-radius: 16px; box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.1); background-color: white">
          <!-- Header -->
          <h2 class="text-center font-weight-bold mb-2" style="font-size: 24px; color: #333">회원가입</h2>
          <p class="text-center mb-6" style="color: #777">회원이 되어 다양한 혜택을 경험해 보세요!</p>

          <!-- Form -->
          <v-form @submit.prevent="handleSignup" v-model="isValid">
            <!-- 아이디 -->
            <v-text-field v-model="username" label="아이디 입력 (6~20자)" outlined dense class="mb-4" :rules="[(v) => !!v || '아이디를 입력해주세요']" style="border-radius: 8px" />
            <!-- 비밀번호 -->
            <v-text-field v-model="password1" label="비밀번호 입력 (8~20자)" type="password" outlined dense class="mb-4" :rules="passwordRules" style="border-radius: 8px" />
            <!-- 비밀번호 확인 -->
            <v-text-field
              v-model="password2"
              label="비밀번호 확인"
              type="password"
              outlined
              dense
              class="mb-4"
              :rules="[(v) => v === password1 || '비밀번호가 일치하지 않습니다']"
              style="border-radius: 8px"
            />
            <!-- 닉네임 -->
            <v-text-field v-model="nickname" label="닉네임 입력" outlined dense class="mb-4" :rules="[(v) => !!v || '닉네임을 입력해주세요']" style="border-radius: 8px" />
            <!-- 나이 -->
            <v-text-field
              v-model="age"
              label="나이 입력 (숫자만)"
              outlined
              dense
              class="mb-4"
              :rules="[(v) => !!v || '나이를 입력해주세요']"
              oninput="javascript: this.value = this.value.replace(/\D/g, '')"
              style="border-radius: 8px"
            />
            <!-- 자본금 -->
            <v-text-field
              v-model="capital"
              label="자본금 입력 (숫자만)"
              outlined
              dense
              class="mb-4"
              suffix="만원"
              :rules="[(v) => !!v || '자본금을 입력해주세요']"
              oninput="javascript: this.value = this.value.replace(/\D/g, '')"
              style="border-radius: 8px"
            />
            <!-- 시/도 선택 -->
            <v-select
              v-model="sido"
              :items="sidoList"
              label="시/도 선택"
              outlined
              dense
              class="mb-4"
              :rules="[(v) => !!v || '시/도를 선택해주세요']"
              style="border-radius: 8px"
              @change="onSidoChange"
            />
            <!-- 시/군/구 선택 -->
            <v-select
              v-model="sigugun"
              :items="sigugunList"
              label="시/군/구 선택"
              outlined
              dense
              class="mb-6"
              :rules="[(v) => !!v || '시/군/구를 선택해주세요']"
              :disabled="!sigugunList.length"
              style="border-radius: 8px"
            />

            <!-- Buttons -->
            <v-btn
              :disabled="!isValid"
              color="primary"
              block
              type="submit"
              :loading="isSubmitting"
              class="py-3 font-weight-bold"
              style="border-radius: 8px; background-color: #1e88e5; color: white; font-size: 16px"
            >
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

const { signUp } = useAccount();
const addressStore = useAddressStore();

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

const passwordRules = [
  (v) => !!v || "비밀번호를 입력해주세요.",
  (v) => v.length >= 8 || "비밀번호는 최소 8자 이상이어야 합니다.",
  // (v) => /[A-Z]/.test(v) || "비밀번호는 대문자를 하나 이상 포함해야 합니다.",
  // (v) => /[a-z]/.test(v) || "비밀번호는 소문자를 하나 이상 포함해야 합니다.",
  // (v) => /[0-9]/.test(v) || "비밀번호는 숫자를 하나 이상 포함해야 합니다.",
  (v) => /[!@#$%^&*(),.?":{}|<>]/.test(v) || "비밀번호는 특수문자를 하나 이상 포함해야 합니다.",
];

const sidoList = computed(() => addressStore.address_infos.map((info) => info.sido));
const sigugunList = computed(() => {
  const selectedSido = addressStore.address_infos.find((info) => info.sido === sido.value);
  return selectedSido ? selectedSido.sigungus : [];
});

const onSidoChange = () => {
  sigugun.value = null;
};

const handleSignup = async () => {
  console.log({
    nickname: nickname.value,
    sigugun: sigugun.value,
  });
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
    alert("회원가입 성공!");
  } catch (error) {
    console.error("회원가입 실패:", error);
  } finally {
    isSubmitting.value = false;
  }
};
</script>
