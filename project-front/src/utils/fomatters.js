// 숫자 포맷팅 함수
export const numberFormat = (value) => {
    return new Intl.NumberFormat("ko-KR").format(value);
};

// 등락률에 따른 클래스 반환
export const getChangeClass = (change) => {
    return change >= 0 ? "red--text" : "blue--text";
};