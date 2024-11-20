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

            response_text = initial_prompt + "\n\n"  # 초기 프롬프트 포함

            if product_type is not None and term is not None:
                products = FinancialProducts.objects.filter(product_type=product_type)
                if products.exists():
                    filtered_products = []
                    for product in products:
                        options = FinancialOptions.objects.filter(product=product, save_trm=term)
                        if options.exists():
                            filtered_products.append({
                                "product_name": product.fin_prdt_nm,
                                "company": product.kor_co_nm,
                                "interest_rate": options[0].intr_rate,
                                "term": term
                            })
                    if filtered_products:
                        product_text_list = [
                            f"{p['company']}의 {p['product_name']} (이자율: {p['interest_rate']}%, 기간: {p['term']}개월)"
                            for p in filtered_products
                        ]
                        response_text += "다음과 같은 적합한 금융 상품을 추천드립니다: " + ", ".join(product_text_list)
                    else:
                        response_text += "조건에 맞는 금융 상품이 없습니다. 다른 조건으로 다시 시도해주세요."
                else:
                    response_text += "조건에 맞는 금융 상품이 없습니다. 다른 조건으로 다시 시도해주세요."
            else:
                response_text += "조금 더 구체적으로 입력해 주세요. 예를 들어, '300만원을 24개월 동안 적금하려고 하는데 추천 상품이 있을까요?'와 같이 말해 보세요."

            # OpenAI API에 응답 요청
            try:
                    # prompt=response_text,
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": initial_prompt},
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": response_text},
                    ],
                    stream= True,
                    temperature=0.7,
                )
                gpt_response = ""
                # print(response)
                for chunk in response:
                    content_part = chunk.choices[0].delta.content  # content_part 추출
                    if content_part is not None:  # content_part가 None이 아닌지 확인
                        gpt_response += content_part

                print(gpt_response)
                
                return JsonResponse({'response': gpt_response})

            except OpenAIError as e:  # 올바른 예외 클래스 사용
                return JsonResponse({'error': f'OpenAI API 호출 중 문제가 발생했습니다: {str(e)}'}, status=500)

        except json.JSONDecodeError:  # JSON 파싱 오류 처리 추가
            return JsonResponse({'error': '유효하지 않은 JSON 형식입니다.'}, status=400)
        except Exception as e:  # 일반 오류 처리 강화
            return JsonResponse({'error': f'서버 내부 오류가 발생했습니다: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
