<template>
  <v-container class="fill-height" style="background-color: #f9fafb">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="6">
        <v-card class="pa-6" style="border-radius: 16px; box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.1); background-color: white">
          <h2 class="text-center font-weight-bold mb-4" style="font-size: 24px; color: #333">게시글 작성</h2>
          <p class="text-center mb-6" style="color: #777">새로운 게시글을 작성해 주세요!</p>

          <!-- Form -->
          <v-form @submit.prevent="handleSubmit" v-model="isValid">
            <!-- 제목 -->
            <v-text-field v-model="title" label="제목" outlined dense class="mb-4" :rules="[(v) => !!v || '제목을 입력해주세요.']" style="border-radius: 8px" />

            <!-- 내용 -->
            <v-textarea v-model="content" label="내용" outlined dense rows="6" class="mb-4" :rules="[(v) => !!v || '내용을 입력해주세요.']" style="border-radius: 8px" />

            <!-- 등록 버튼 -->
            <v-btn
              :disabled="!isValid"
              color="primary"
              block
              type="submit"
              :loading="isSubmitting"
              class="py-3 font-weight-bold"
              style="border-radius: 8px; background-color: #1e88e5; color: white; font-size: 16px"
            >
              등록하기
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useAccount } from "@/stores/accounts";

const API_URL = "http://127.0.0.1:8000"; // API URL

// Vue Router 사용
const router = useRouter();

// 게시글 데이터
const title = ref("");
const content = ref("");
const isValid = ref(false);
const isSubmitting = ref(false);

// 게시글 등록 핸들러
const handleSubmit = async () => {
  isSubmitting.value = true;
  try {
    const accountStore = useAccount();
    const token = accountStore.token;
    const response = await axios.post(
      `${API_URL}/api/articles/create/`,
      {
        title: title.value,
        content: content.value,
        users: accountStore.users,
      },
      {
        headers: {
          Authorization: `Token ${token}`,
        },
      }
    );

    console.log("게시글 생성 완료:", response.data);
    alert("게시글 생성 완료!");
    router.push({ name: "community" }); // 게시판 페이지로 이동
  } catch (error) {
    console.error("게시글 등록 실패:", error);
    alert("게시글 등록에 실패했습니다. 다시 시도해주세요.");
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
h2 {
  font-size: 24px;
  color: #333;
}

.v-card {
  max-width: 600px;
}
</style>
