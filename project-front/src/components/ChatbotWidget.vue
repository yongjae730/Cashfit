<template>
    <div>
      <!-- 챗봇 팝업 창 -->
      <div v-if="showChatbot" class="chatbot-window">
        <div class="chatbot-header">
          <h4>금융 챗봇</h4>
          <button @click="toggleChatbot" class="close-btn">X</button>
        </div>
        <div class="chatbot-body">
          <div v-for="(message, index) in messages" :key="index" class="message">
            <p :class="message.sender">{{ message.text }}</p>
          </div>
          <div v-if="loading" class="loading-message">답변을 기다리는 중...</div>
          <input v-model="userInput" @keyup.enter="sendMessage" placeholder="질문을 입력하세요..." class="input-box" />
        </div>
      </div>
  
      <!-- 우하단 챗봇 버튼 -->
      <button @click="toggleChatbot" class="chatbot-button">💬</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  
  // 컴포넌트 상태 관리
  const showChatbot = ref(false)
  const messages = ref([])
  const userInput = ref('')
  const loading = ref(false)  // 로딩 상태 관리 변수
  const userId = ref(1)  // 유저 ID를 저장 (로그인된 유저의 ID로 설정)
  
  // 챗봇 열기/닫기 토글
  const toggleChatbot = () => {
    showChatbot.value = !showChatbot.value
  }
  
  // 메시지 전송 로직
  const sendMessage = async () => {
    if (userInput.value.trim() === '') return
  
    // 사용자 메시지 추가
    messages.value.push({ sender: 'user', text: userInput.value })
  
    // 로딩 상태로 전환
    loading.value = true
  
    try {
      // Flask 서버에 사용자 입력 전송
      const response = await axios.post('http://localhost:5000/chat', {
        user_id: userId.value,
        message: userInput.value
      })
  
      // 챗봇 응답 추가
      messages.value.push({ sender: 'bot', text: response.data.response })
    } catch (error) {
      console.error('Error communicating with the chatbot:', error)
      messages.value.push({ sender: 'bot', text: '답변을 가져오는 데 실패했습니다.' })
    } finally {
      // 로딩 상태 해제
      loading.value = false
    }
  
    userInput.value = ''
  }
  </script>
  
  <style scoped>
  /* 우하단 챗봇 버튼 스타일 */
  .chatbot-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  /* 챗봇 창 스타일 */
  .chatbot-window {
    position: fixed;
    bottom: 100px;
    right: 20px;
    width: 300px;
    height: 400px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  /* 챗봇 헤더 */
  .chatbot-header {
    background-color: #007bff;
    color: white;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  /* 챗봇 메시지 */
  .chatbot-body {
    flex: 1;
    padding: 10px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }
  
  .message {
    margin: 5px 0;
  }
  
  .user {
    text-align: right;
    color: blue;
  }
  
  .bot {
    text-align: left;
    color: green;
  }
  
  .loading-message {
    text-align: center;
    color: grey;
    margin: 10px 0;
  }
  
  .input-box {
    padding: 10px;
    border-top: 1px solid #ddd;
    width: calc(100% - 20px);
    margin: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  </style>
  