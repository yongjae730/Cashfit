<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="pa-4" elevation="2">
          <h3 class="text-center mb-4">회원가입</h3>
          <v-form @submit.prevent="handleSignup" v-model="isValid">
            <v-text-field v-model="username" label="아이디" required :rules="[(v) => !!v || '아이디를 입력해주세요']" class="mb-4" />
            <v-text-field
              v-model="password1"
              label="비밀번호"
              type="password"
              required
              :rules="[(v) => !!v || '비밀번호를 입력해주세요', (v) => v.length >= 8 || '8자 이상이어야 합니다']"
              class="mb-4"
            />
            <v-text-field v-model="password2" label="비밀번호 확인" type="password" required :rules="[(v) => v === password1 || '비밀번호 일치하지 않습니다']" class="mb-4" />
            <!-- 닉네임 -->
            <v-text-field v-model="nickname" label="닉네임 입력" required :rules="[(v) => !!v || '닉네임을 입력해주세요']" class="mb-4" />
            <!-- 나이 -->
            <v-text-field v-model="age" label="나이 입력" required :rules="[(v) => !!v || '나이를 입력해주세요']" oninput="javascript: this.value = this.value.replace(/\D/g, '')" class="mb-4" />

            <!-- 수입 -->
            <v-text-field v-model="capital" label="자본금" required :rules="[(v) => !!v || '자본금을 입력해주세요']" oninput="javascript: this.value = this.value.replace(/\D/g, '')" class="mb-4" />

            <!-- 시/도 선택 -->
            <v-select v-model="sido" :items="sidoList" label="시/도 선택" required :rules="[(v) => !!v || '시/도를 선택해주세요']" class="mb-4" @change="onSidoChange" />
            <!-- 시/군/구 선택-->
            <v-select v-model="sigugun" :items="sigugunList" label="시/군/구 선택" required :rules="[(v) => !!v || '시/군/구를 선택해주세요']" class="mb-4" :disabled="!sigugunList.length" />
            <v-btn :disabled="!isValid" color="primary" block type="submit" :loading="isSubmitting">가입하기</v-btn>
          </v-form>
          <v-divider class="my-4"><span>또는</span></v-divider>
          <v-btn block color="secondary" @click="showLoginModal = true">로그인하기</v-btn>
        </v-card>
      </v-col>
    </v-row>

    <LoginModal :is-open="showLoginModal" @update:is-open="showLoginModal = $event" />
  </v-container>
</template>

<script setup>
import { computed, ref } from "vue";
import LoginModal from "@/components/LoginModal.vue";
import { useAccount } from "@/stores/accounts";
import { useAddressStore } from "@/stores/address";

const { signUp } = useAccount();

const addressStore = useAddressStore();

const username = ref("");
const password1 = ref("");
const password2 = ref("");
const age = ref("");
const nickname = ref("");
const capital = ref("");
const isValid = ref(false);
const isSubmitting = ref(false);

const sido = ref(null);
const sigugun = ref(null);

const sidoList = computed(() => addressStore.address_infos.map((info) => info.sido));
const sigugunList = computed(() => {
  const selectedSido = addressStore.address_infos.find((info) => info.sido === sido.value);
  return selectedSido ? selectedSido.sigungus : [];
});

const onSidoChange = () => {
  sigugun.value = null;
};

const showLoginModal = ref(false);

const handleSignup = async () => {
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
      siguguns: sigugun.value,
    });
    console.log("회원가입 성공");
  } catch (err) {
    console.error("회원가입 실패:", err);
  } finally {
    isSubmitting.value = false;
  }
};
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
