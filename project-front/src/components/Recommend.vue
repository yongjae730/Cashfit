<template>
    <v-card style="margin: 10px" class="my-6 info-card">
        <v-card-title class="d-flex align-center font-weight-bold text-h6">
            맞춤 적금 상품
            <v-spacer></v-spacer>
            <v-chip color="primary" class="ml-2">
                {{ userInfo.age }}세 맞춤
            </v-chip>
        </v-card-title>

        <v-card-text>
            <div v-if="recommendations.length" class="recommendation-container">
                <v-slide-group show-arrows>
                    <v-slide-item v-for="(product, index) in recommendations" :key="index">
                        <v-card width="400" class="ma-2 product-recommendation-card">
                            <v-card-title class="bank-info d-flex align-center">
                                <div class="bank-logo-container mr-3">
                                    <v-img :src="`/bank_images/${product.kor_co_nm}.jpg`"
                                        :error-src="`/bank_images/default.jpg`" class="bank-logo" cover alt="상품 이미지">
                                    </v-img>
                                </div>
                                <span class="bank-name">{{ product.kor_co_nm }}</span>
                            </v-card-title>

                            <v-card-title class="product-title pt-0">
                                {{ product.fin_prdt_nm }}
                            </v-card-title>

                            <v-card-text>
                                <v-list dense>
                                    <v-list-item>
                                        <v-list-item-title>
                                            <v-icon small color="green">mdi-chart-line</v-icon>
                                            최고금리: {{ getMaxInterestRate(product.options) }}%
                                        </v-list-item-title>
                                    </v-list-item>
                                    <v-list-item>
                                        <v-list-item-title>
                                            <v-icon small color="blue">mdi-calendar-clock</v-icon>
                                            가입기간: {{ getTermRange(product.options) }}
                                        </v-list-item-title>
                                    </v-list-item>
                                </v-list>
                            </v-card-text>

                            <v-card-actions>
                                <v-btn color="primary" text block @click="toggleLike(product.id)">
                                    <v-icon left :color="isProductLiked(product.id) ? 'red' : 'gray'">
                                        {{ isProductLiked(product.id) ? 'mdi-heart' : 'mdi-heart-outline' }}
                                    </v-icon>
                                    {{ isProductLiked(product.id) ? '찜해제' : '찜하기' }}
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-slide-item>
                </v-slide-group>
            </div>
            <div v-else class="empty-state">
                현재 추천 가능한 상품이 없습니다.
            </div>
        </v-card-text>
    </v-card>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAccount } from "@/stores/accounts";
import axios from 'axios';

const accountStore = useAccount();
const recommendations = ref([]);
const API_URL = "http://127.0.0.1:8000";

const userInfo = computed(() => accountStore.user?.user_info || {});

// 상품 추천 데이터 가져오기
const fetchRecommendations = async () => {
    try {
        const headers = {
            Authorization: `Token ${accountStore.token}`,
        };
        const response = await axios.get(
            `${API_URL}/api/financials/recommendations/age/`,
            { headers }
        );
        recommendations.value = response.data.recommendations;
    } catch (error) {
        console.error('추천 상품 조회 실패:', error);
    }
};

// 최고 금리 계산
const getMaxInterestRate = (options) => {
    if (!options || !options.length) return '0.0';
    return Math.max(...options.map(opt => opt.intr_rate2)).toFixed(1);
};

// 가입기간 범위 계산
const getTermRange = (options) => {
    if (!options || !options.length) return '정보없음';
    const terms = options.map(opt => opt.save_trm);
    const minTerm = Math.min(...terms);
    const maxTerm = Math.max(...terms);
    return minTerm === maxTerm ?
        `${minTerm}개월` :
        `${minTerm}~${maxTerm}개월`;
};

// 좋아요 여부 확인
const isProductLiked = (productId) => {
    return accountStore.user?.liked_products?.some(
        product => product.id === productId
    ) || false;
};

// 좋아요 추가
const toggleLike = async (productId) => {
    try {
        const headers = {
            Authorization: `Token ${accountStore.token}`,
        };

        if (isProductLiked(productId)) {
            // 이미 좋아요 상태면 제거
            await axios.delete(
                `${API_URL}/api/financials/products/${productId}/like/`,
                { headers }
            );
        } else {
            // 좋아요 상태가 아니면 추가
            await axios.post(
                `${API_URL}/api/financials/products/${productId}/like/`,
                {},
                { headers }
            );
        }

        // 프로필 정보 업데이트 (좋아요 목록 갱신)
        await accountStore.getProfile();

        // 선택적: 성공 메시지 표시
        const message = isProductLiked(productId) ? '찜하기 완료되었습니다.' : '찜해제 되었습니다.';
        // 만약 sweet alert를 사용중이라면:
        swal({
            text: message,
            icon: "success",
            buttons: false,
            timer: 1000,
        });

    } catch (error) {
        console.error('좋아요 토글 실패:', error);
        // 에러 메시지 표시
        swal({
            title: "오류",
            text: "처리 중 문제가 발생했습니다.",
            icon: "error",
            button: "확인",
        });
    }
};

onMounted(fetchRecommendations);
</script>

<style scoped>
.product-recommendation-card {
    transition: transform 0.2s;
    height: 100%;
}

.product-recommendation-card:hover {
    transform: translateY(-4px);
}

.recommendation-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.bank-name {
    font-size: 1rem;
    font-weight: bold;
    color: #3f51b5;
    margin-left: 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.product-title {
    font-size: 1rem;
    line-height: 1.4;
    height: 2.8em;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.bank-logo-container {
    width: 150px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    border-radius: 4px;
    overflow: hidden;
    padding: 4px;
    /* 패딩 추가 */
}

.bank-logo {
    max-width: 100%;
    /* width: 150px 대신 */
    max-height: 100%;
    /* height: 40px 대신 */
    width: auto;
    /* 추가 */
    height: auto;
    /* 추가 */
    object-fit: contain;
    background-color: white;
    display: block;
    /* 추가 */
}

/* 필요한 경우 bank-info의 패딩도 조정 */
.bank-info {
    min-height: 60px;
    padding: 12px;
    /* 8px에서 증가 */
    display: flex;
    align-items: center;
}


/* 선택적: 좋아요 버튼에 호버 효과 추가 */
.v-btn:hover {
    opacity: 0.8;
    transform: scale(1.02);
}

/* 선택적: 좋아요 아이콘 애니메이션 */
.v-icon {
    transition: transform 0.2s ease;
}

.v-btn:hover .v-icon {
    transform: scale(1.1);
}
</style>