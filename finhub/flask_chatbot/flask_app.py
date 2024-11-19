import os
from flask import Flask, request, jsonify
import openai
import requests
from flask_cors import CORS
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)
CORS(app)

# OpenAI API 키 설정 (환경 변수에서 가져오기)
openai.api_key = os.getenv('OPENAI_API_KEY')

# API 키가 제대로 로드되었는지 확인
if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Please check your .env file.")

# Django API 엔드포인트 설정
DJANGO_BASE_URL = "http://localhost:8000"
DJANGO_LOGIN_URL = f"{DJANGO_BASE_URL}/accounts/login/"
DJANGO_FINANCIALS_URL = f"{DJANGO_BASE_URL}/api/financials/"

# 로그인 세션 관리
session_data = requests.Session()
auth_token = None

@app.route("/login", methods=["POST"])
def login_to_django():
    global auth_token
    # 사용자가 전달한 로그인 데이터 받기
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Django로 로그인 요청 보내기
    login_data = {
        'username': username,
        'password': password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = session_data.post(DJANGO_LOGIN_URL, json=login_data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to log in to Django: {response.status_code} - {response.text}")

        # 로그인 성공 시 토큰 저장
        response_data = response.json()
        auth_token = response_data.get('key')  # dj-rest-auth는 기본적으로 'key'라는 필드에 토큰을 반환
        if not auth_token:
            raise Exception("Failed to obtain token from Django login response")
        
        # 디버깅: 받은 토큰 출력
        print(f"Received Token: {auth_token}")

        # 세션에 토큰 추가
        session_data.headers.update({'Authorization': f'Token {auth_token}'})
        return jsonify({"message": "Login successful"}), 200

    except Exception as e:
        print(f"Error occurred during login: {str(e)}")  # 오류 로그 출력
        return jsonify({"error": str(e)}), 500
    

@app.route("/chat", methods=["POST"])
def chat():
    global auth_token
    user_message = request.json.get("message")

    # 메시지가 비어 있는지 확인
    if not user_message:
        return jsonify({"error": "Message field is required"}), 400

    # 로그인되지 않은 경우 401 에러 반환
    if not auth_token:
        return jsonify({"error": "User is not authenticated"}), 401

    try:
        # Django에서 사용자 정보 가져오기 (인증 헤더 추가)
        headers = {
            'Authorization': f'Token {auth_token}'
        }

        # 사용자 정보 요청 시 인증 헤더 포함
        user_info_response = requests.get(f"{DJANGO_FINANCIALS_URL}/get-user-info/", headers=headers)
        if user_info_response.status_code != 200:
            raise Exception(f"Failed to fetch user info: {user_info_response.status_code} - {user_info_response.text}")
        user_info = user_info_response.json()

        # 금융 상품 정보 요청 시 인증 헤더 포함
        financial_products_response = requests.get(f"{DJANGO_FINANCIALS_URL}/get-financial-products/", headers=headers)
        if financial_products_response.status_code != 200:
            raise Exception(f"Failed to fetch financial products: {financial_products_response.status_code} - {financial_products_response.text}")
        financial_products = financial_products_response.json().get("products", [])

        # 대화 컨텍스트 생성
        context = f"사용자 정보: {user_info}\n금융 상품 목록 및 옵션: {financial_products}\n"
        context += f"사용자 질문: {user_message}\n"
        context += (
            "각 금융 상품의 옵션에는 금리 유형, 저축 금리, 최고 우대 금리, 저축 기간 등의 정보가 포함되어 있습니다. "
            "사용자에게 가장 유리한 금융 상품을 추천하는 답변을 작성하세요."
        )

        # GPT-4-turbo 모델을 사용해 응답 생성
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "당신은 금융 전문가 챗봇입니다. 사용자 정보를 바탕으로 개인 맞춤형 금융 상품 옵션을 추천하세요."},
                {"role": "user", "content": context}
            ],
            max_tokens=200,
            temperature=0.7
        )
        chatbot_response = response['choices'][0]['message']['content']

        # 응답 반환
        return jsonify({"response": chatbot_response})

    except Exception as e:
        # 자세한 오류 로그를 출력합니다.
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 서버 실행
    app.run(port=5000, debug=True)
