<template>
  <div class="chatbot-widget">
    <!-- 챗봇 아이콘 -->
    <div v-if="!isOpen" class="chat-icon" @click="toggleChat">💬</div>

    <!-- 챗봇 창 -->
    <div v-if="isOpen" class="chat-window">
      <div class="chat-header">
        <span>금융 상담 챗봇</span>
        <button @click="toggleChat">X</button>
      </div>
      <div class="chat-content">
        <div v-for="(msg, index) in messages" :key="index" class="message">
          <div :class="msg.type" v-html="msg.text"></div>
        </div>
        <div v-if="isWaiting" class="message bot">{{ waitingMessage }}</div>
      </div>
      <div class="chat-input">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="메시지를 입력하세요..." />
        <button @click="sendMessage">전송</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const isOpen = ref(false);
const userInput = ref("");
const messages = ref([{ type: "bot", text: "안녕하세요! 예금이나 적금 상품에 대해 궁금한 점을 말씀해주세요." }]);
const isWaiting = ref(false);
const waitingMessage = ref("답변 기다리는중 ...");

// 채팅창 열기/닫기
const toggleChat = () => {
  isOpen.value = !isOpen.value;
};

// 대기 메시지 애니메이션 설정
let waitingInterval;
const startWaitingAnimation = () => {
  let dots = 0;
  waitingInterval = setInterval(() => {
    dots = (dots + 1) % 4;
    waitingMessage.value = "답변 기다리는중" + ".".repeat(dots);
  }, 500);
};

const stopWaitingAnimation = () => {
  clearInterval(waitingInterval);
  waitingMessage.value = "답변 기다리는중 ...";
};

// 메시지 전송 함수
const sendMessage = async () => {
  if (userInput.value.trim() !== "") {
    // 사용자가 입력한 메시지 추가
    messages.value.push({ type: "user", text: userInput.value });

    // 응답 대기 메시지 추가
    isWaiting.value = true;
    startWaitingAnimation();

    // 서버에 메시지 전송
    try {
      const response = await axios.post(
        "http://localhost:8000/chatbot/get-response/",
        {
          message: userInput.value,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      // 응답 대기 메시지 삭제
      isWaiting.value = false;
      stopWaitingAnimation();
      messages.value = messages.value.filter((msg) => msg.text !== "답변 기다리는중 ...");

      // 서버로부터 받은 응답 추가
      messages.value.push({ type: "bot", text: response.data.response.replace(/\n/g, "<br>") });
    } catch (error) {
      // 응답 대기 메시지 삭제
      isWaiting.value = false;
      stopWaitingAnimation();
      messages.value = messages.value.filter((msg) => msg.text !== "답변 기다리는중 ...");

      if (error.response) {
        // 서버에서 오류 응답을 받은 경우
        console.error("서버 오류:", error.response.data);
        messages.value.push({ type: "bot", text: "서버 오류가 발생했습니다. 다시 시도해주세요." });
      } else if (error.request) {
        // 요청이 보내졌으나 응답이 없는 경우
        console.error("서버로부터 응답이 없습니다.");
        messages.value.push({ type: "bot", text: "서버로부터 응답이 없습니다. 인터넷 연결을 확인해주세요." });
      } else {
        // 기타 오류
        console.error("오류:", error.message);
        messages.value.push({ type: "bot", text: "알 수 없는 오류가 발생했습니다. 다시 시도해주세요." });
      }
    } finally {
      userInput.value = "";
    }
  }
};
</script>

<style scoped>
.chatbot-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chat-icon {
  width: 60px;
  height: 60px;
  background-color: #007bff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.chat-window {
  width: 400px;
  height: 600px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.chat-header {
  padding: 10px;
  background-color: #007bff;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.chat-content {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background-color: #f9f9f9;
}

.message {
  margin-bottom: 10px;
  font-size: 14px;
}

.user {
  text-align: right;
  color: blue;
}

.bot {
  text-align: left;
  color: green;
}

.chat-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ccc;
  background-color: #f9f9f9;
}

input {
  flex: 1;
  padding: 10px;
  margin-right: 10px;
}

button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
