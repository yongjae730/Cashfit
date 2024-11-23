<template>
  <div class="chatbot-widget">
    <!-- 챗봇 아이콘 -->
    <div v-if="!isOpen" class="chat-icon" @click="toggleChat">💬</div>

    <!-- 챗봇 창 -->
    <div v-if="isOpen" class="chat-window" ref="chatWindow">
      <!-- 좌상단 커스텀 크기 조절 핸들 -->
      <div class="resize-handle" @mousedown="startResizing"></div>
      <div class="chat-header">
        <span>캐시피터</span>
        <button @click="toggleChat">X</button>
      </div>
      <div ref="chatContent" class="chat-content">
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
import { ref, watchEffect, onMounted, onUnmounted } from "vue";
import axios from "axios";

const isOpen = ref(false);
const userInput = ref("");
const messages = ref([{ type: "bot", text: "안녕하세요! 예금이나 적금 상품에 대해 궁금한 점을 말씀해주세요." }]);
const isWaiting = ref(false);
const waitingMessage = ref("답변 기다리는중 ...");
const chatContent = ref(null);
const chatWindow = ref(null);

let isResizing = false;
let startX = 0;
let startY = 0;
let startWidth = 0;
let startHeight = 0;

// 메시지가 추가될 때마다 스크롤을 맨 아래로 이동
watchEffect(() => {
  if (messages.value.length && chatContent.value) {
    setTimeout(() => {
      chatContent.value.scrollTop = chatContent.value.scrollHeight;
    }, 100);
  }
});

// 채팅창 열기/닫기
const toggleChat = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    setTimeout(() => {
      if (chatContent.value) {
        chatContent.value.scrollTop = chatContent.value.scrollHeight;
      }
    }, 100);
  }
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
    messages.value.push({ type: "user", text: userInput.value });
    isWaiting.value = true;
    startWaitingAnimation();

    try {
      const response = await axios.post("http://localhost:8000/chatbot/get-response/", { message: userInput.value }, { headers: { "Content-Type": "application/json" } });
      isWaiting.value = false;
      stopWaitingAnimation();
      messages.value = messages.value.filter((msg) => msg.text !== "답변 기다리는중 ...");
      messages.value.push({ type: "bot", text: response.data.response.replace(/\n/g, "<br>") });
    } catch (error) {
      isWaiting.value = false;
      stopWaitingAnimation();
      messages.value = messages.value.filter((msg) => msg.text !== "답변 기다리는중 ...");

      if (error.response) {
        console.error("서버 오류:", error.response.data);
        messages.value.push({ type: "bot", text: "서버 오류가 발생했습니다. 다시 시도해주세요." });
      } else if (error.request) {
        console.error("서버로부터 응답이 없습니다.");
        messages.value.push({ type: "bot", text: "서버로부터 응답이 없습니다. 인터넷 연결을 확인해주세요." });
      } else {
        console.error("오류:", error.message);
        messages.value.push({ type: "bot", text: "알 수 없는 오류가 발생했습니다. 다시 시도해주세요." });
      }
    } finally {
      userInput.value = "";
    }
  }
};

// 크기 조절 시작
const startResizing = (e) => {
  isResizing = true;
  startX = e.clientX;
  startY = e.clientY;
  startWidth = chatWindow.value.offsetWidth;
  startHeight = chatWindow.value.offsetHeight;

  document.addEventListener("mousemove", resize);
  document.addEventListener("mouseup", stopResizing);
};

// 크기 조절 중
const resize = (e) => {
  if (isResizing) {
    const newWidth = Math.max(300, Math.min(1200, startWidth - (e.clientX - startX)));
    const newHeight = Math.max(400, Math.min(1800, startHeight - (e.clientY - startY)));
    chatWindow.value.style.width = `${newWidth}px`;
    chatWindow.value.style.height = `${newHeight}px`;
  }
};

// 크기 조절 종료
const stopResizing = () => {
  isResizing = false;
  document.removeEventListener("mousemove", resize);
  document.removeEventListener("mouseup", stopResizing);
};

onMounted(() => {
  document.addEventListener("mouseup", stopResizing);
});

onUnmounted(() => {
  document.removeEventListener("mouseup", stopResizing);
});
</script>

<style scoped>
.chatbot-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: "Noto Sans KR", sans-serif;
}

.chat-icon {
  width: 60px;
  height: 60px;
  background-color: #2563eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 24px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.chat-icon:hover {
  transform: scale(1.1);
}

.chat-window {
  width: 395px;
  height: 500px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: auto;
  min-width: 300px;
  min-height: 400px;
  max-width: 1200px;
  max-height: 1800px;
}

/* 좌상단 크기 조절 핸들 */
.resize-handle {
  position: absolute;
  top: -6px;
  left: -6px;
  width: 12px;
  height: 12px;
  background-color: #2563eb;
  border-radius: 50%;
  cursor: nwse-resize; /* 대각선 크기 조절 커서 */
  z-index: 1001;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.chat-header {
  background-color: #2563eb;
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.chat-header button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 18px;
}

.chat-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto; /* 내부 콘텐츠 스크롤 가능 */
  background-color: #f8fafc;
  scroll-behavior: smooth;
}

.message {
  margin: 8px 0;
  display: flex;
  flex-direction: column;
  font-size: 14px;
}

.bot,
.user {
  max-width: 80%;
  padding: 12px;
  border-radius: 12px;
  margin: 4px 0;
  position: relative;
  word-wrap: break-word;
}

.bot {
  background-color: #e2e8f0;
  color: #1e293b;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.bot::before {
  content: "";
  position: absolute;
  left: -6px;
  bottom: 0;
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, #e2e8f0 50%, transparent 50%);
}

.user {
  background-color: #2563eb;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.user::before {
  content: "";
  position: absolute;
  right: -6px;
  bottom: 0;
  width: 12px;
  height: 12px;
  background: linear-gradient(-45deg, #2563eb 50%, transparent 50%);
}

.chat-input {
  padding: 16px;
  background-color: white;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 8px;
}

.chat-input input {
  flex: 1;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  outline: none;
  font-size: 14px;
}

.chat-input input:focus {
  border-color: #2563eb;
}

.chat-input button {
  padding: 12px 20px;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.chat-input button:hover {
  background-color: #1d4ed8;
}

/* 스크롤바 스타일링 */
.chat-content::-webkit-scrollbar {
  width: 6px;
}

.chat-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-content::-webkit-scrollbar-thumb {
  background: #becde3;
  border-radius: 3px;
}

.chat-content::-webkit-scrollbar-thumb:hover {
  background: #8ba2c5;
}
</style>
