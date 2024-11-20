from django.shortcuts import render
from openai import OpenAIError
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
import re
from financials.models import FinancialProducts, FinancialOptions
import os
from dotenv import load_dotenv
from openai import OpenAI
# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:  # 수정사항: 환경 변수에서 API 키를 읽어올 수 없는 경우 오류 발생
    raise ValueError("OpenAI API key is not set. Please check your .env file.")
openai.api_key = OPENAI_API_KEY

# 금융 전문가 초기 프롬프트 설정
initial_prompt = (
    "당신은 예금 및 적금 상품에 대해 전문적인 지식을 가진 금융 전문가입니다. "
    "사용자에게 이러한 금융 상품에 대한 최상의 정보를 제공하는 것이 당신의 역할입니다. "
    "금리, 기간, 자격 조건 등을 설명하고, 적합한 금융 상품을 추천하는 업무를 수행합니다. "
    "항상 친절하고 명확하며 전문가다운 어조로 답변해 주세요."
)
client = OpenAI()

@csrf_exempt  # CSRF 검증 비활성화 (테스트 시에만 사용, 실제 서비스에서는 CSRF 보호 사용 권장)
def chatbot_response(request):
    # POST 요청을 통해 데이터를 수신
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('message')

            if not user_input:  # 수정사항: 입력 메시지가 비어 있는 경우에 대한 구체적인 오류 처리 추가
                return JsonResponse({'error': '메시지가 비어있습니다.'}, status=400)
             # 세션에서 이전 대화 내역 가져오기 - 수정사항 시작
            if 'chat_history' not in request.session:
                request.session['chat_history'] = []  # 수정사항: 세션에 'chat_history'가 없을 경우 빈 리스트로 초기화

            # 현재 세션의 대화 내역을 가져와 GPT 모델 입력 메시지로 사용
            previous_messages = request.session['chat_history']
            previous_messages.append({"role": "user", "content": user_input})  # 수정사항: 사용자의 입력 메시지를 세션에 추가
            # 수정사항 끝: 세션을 사용하여 대화 내역 관리

            # 사용자 입력으로부터 금액과 기간 정보 추출
            amount_match = re.search(r'(\d+)(만원|백만원|천만원|억)', user_input)
            term_match = re.search(r'(\d+)개월', user_input)

            # 금액 및 기간 파싱
            amount = None
            if amount_match:
                amount = int(amount_match.group(1)) * 10000
            term = None
            if term_match:
                term = int(term_match.group(1))

            # 적금 또는 예금 판단
            product_type = None
            if "적금" in user_input:
                product_type = 1
            elif "예금" in user_input:
                product_type = 0

            # 금융 상품 조회 및 필터링
            recommended_products = []
            if product_type is not None and term is not None:
                products = FinancialProducts.objects.filter(product_type=product_type)
                if products.exists():
                    for product in products:
                        options = FinancialOptions.objects.filter(product=product, save_trm=term)
                        if options.exists():
                            for option in options:  # 각 상품 옵션을 더 자세히 포함
                                recommended_products.append({
                                    "상품명": product.fin_prdt_nm,
                                    "은행": product.kor_co_nm,
                                    "저축 금리": option.intr_rate,
                                    "최고 우대 금리": option.intr_rate2,
                                    "기간": option.save_trm,
                                    "가입 방법": product.join_way,
                                    "가입 대상": product.join_member,
                                    "우대 조건": product.spcl_cnd
                                })
            system_message = initial_prompt

            if recommended_products:
                product_text_list = [
                    (
                        f"{p['은행']}의 {p['상품명']} (기본 금리: {p['저축 금리']}%, "
                        f"최고 우대 금리: {p['최고 우대 금리']}%, 기간: {p['기간']}개월)\n"
                        f"가입 방법: {p['가입 방법']}, 가입 대상: {p['가입 대상']}, 우대 조건: {p['우대 조건']}"
                    )
                    for p in recommended_products
                ]
                system_message += "\n\n현재 추천 가능한 금융 상품 리스트는 다음과 같습니다:\n" + "\n\n".join(product_text_list)
            else:
                system_message += "\n\n현재 사용자의 조건에 맞는 금융 상품을 찾지 못했습니다. 사용자에게 더 나은 추천을 제공하기 위해 추가 정보를 요청하세요."

            # OpenAI API에 응답 요청
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_message},
                        *previous_messages,
                        {"role": "user", "content": user_input},
                    ],
                    stream=True,
                    temperature=0.7,
                )
                gpt_response = ""
                for chunk in response:
                    content_part = chunk.choices[0].delta.content  # content_part 추출
                    if content_part is not None:  # content_part가 None이 아닌지 확인
                        gpt_response += content_part

                # GPT 응답을 세션에 저장 - 수정사항 시작
                previous_messages.append({"role": "assistant", "content": gpt_response})  # 수정사항: GPT의 응답을 세션에 추가
                request.session['chat_history'] = previous_messages  # 수정사항: 세션에 업데이트된 대화 내역 저장
                request.session.modified = True  # 수정사항: 세션 데이터 갱신을 명시적으로 표시

                return JsonResponse({'response': gpt_response})

            except OpenAIError as e:  # 올바른 예외 클래스 사용
                return JsonResponse({'error': f'OpenAI API 호출 중 문제가 발생했습니다: {str(e)}'}, status=500)

        except json.JSONDecodeError:  # JSON 파싱 오류 처리 추가
            return JsonResponse({'error': '유효하지 않은 JSON 형식입니다.'}, status=400)
        except Exception as e:  # 일반 오류 처리 강화
            return JsonResponse({'error': f'서버 내부 오류가 발생했습니다: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
