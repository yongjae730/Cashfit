<template>
  <v-container class="fill-height custom-bg">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="6">
        <!-- 메인 카드 -->
        <v-card class="article-card">
          <!-- 헤더 섹션 -->
          <div class="card-header pa-8 text-center">
            <v-avatar class="mb-4" color="primary" size="56">
              <v-icon icon="mdi-pencil" size="24" color="white" />
            </v-avatar>
            <h2 class="text-h4 font-weight-bold mb-2 gradient-text">게시글 작성</h2>
            <p class="text-subtitle-1 text-medium-emphasis">새로운 게시글을 작성해 주세요!</p>
          </div>

          <v-divider></v-divider>

          <!-- 폼 섹션 -->
          <div class="pa-8">
            <v-form @submit.prevent="handleSubmit" v-model="isValid">
              <!-- 제목 입력 -->
              <v-text-field
                v-model="title"
                label="제목을 입력해주세요"
                variant="outlined"
                :rules="[(v) => !!v || '제목을 입력해주세요.']"
                class="mb-4 custom-field"
                placeholder="제목"
                prepend-inner-icon="mdi-format-title"
              />

              <!-- 내용 입력 -->
              <v-textarea
                v-model="content"
                label="내용을 입력해주세요"
                variant="outlined"
                :rules="[(v) => !!v || '내용을 입력해주세요.']"
                class="mb-6 custom-field"
                placeholder="여기에 내용을 작성해주세요"
                rows="8"
                prepend-inner-icon="mdi-text"
              />

              <!-- 버튼 그룹 -->
              <div class="d-flex button-group">
                <v-btn :disabled="!isValid" color="primary" type="submit" :loading="isSubmitting" class="action-btn flex-grow-1" elevation="0">등록하기</v-btn>
                <v-btn color="grey-lighten-3" @click="router.push({ name: 'community' })" class="cancel-btn ms-3" elevation="0">취소</v-btn>
              </div>
            </v-form>
          </div>
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
import swal from "sweetalert";

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

    await swal({
      title: "성공!",
      text: "게시글이 성공적으로 등록되었습니다.",
      icon: "success",
      button: "확인",
    });
    router.push({ name: "community" }); // 게시판 페이지로 이동
  } catch (error) {
    swal({
      title: "실패 ㅠㅠ",
      text: "게시글 등록에 실패했습니다. 잠시 후 다시 시도해주세요..",
      icon: "error",
      button: "확인",
    });
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

.article-card {
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08) !important;
  overflow: hidden;
  background: white;
  transition: transform 0.3s ease;
}

.article-card:hover {
  transform: translateY(-5px);
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
.action-btn {
  height: 48px;
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

/* 등록 버튼 스타일 */
.action-btn.v-btn--color-primary {
  background: linear-gradient(45deg, #1a237e, #0d47a1);
  color: white;
}

.action-btn.v-btn--disabled {
  opacity: 0.7;
  background: #e2e8f0 !important;
}
.button-group {
  align-items: center;
}

.action-btn {
  height: 48px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-size: 1rem;
  background: linear-gradient(45deg, #1a237e, #0d47a1);
  color: white;
}

.action-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.cancel-btn {
  height: 48px;
  min-width: 100px; /* 취소 버튼의 최소 너비 설정 */
  font-weight: 500;
  letter-spacing: 0.5px;
  text-transform: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  background: #f1f5f9;
  color: #64748b;
}

.cancel-btn:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.action-btn.v-btn--disabled {
  opacity: 0.7;
  background: #e2e8f0 !important;
}
</style>
