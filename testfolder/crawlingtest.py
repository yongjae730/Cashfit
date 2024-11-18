import requests

def get_ticker_price(market):
    url = f"https://api.upbit.com/v1/ticker?markets={market}"
    header = {"accept":"application/json"}
    response = requests.get(url,headers=header)
    data = response.json()
    result = [
        data[0]['trade_price'],
        data[0]['high_price'],
        data[0]['low_price'],
        data[0]['change_rate'],
        data[0]['opening_price'],
    ]
    return result


def get_tickers():
    url = f"https://api.upbit.com/v1/market/all"
    header = {"accept":"application/json"}
    response = requests.get(url,headers=header)
    data = response.json()
    tickers = []
    for market in data:
        if market['market'].startswith("KRW"):
            tickers.append(market['market'])
    return tickers

# 코인 목록 출력
def main():
    tickers = get_tickers()
    
    # for ticker in tickers:
    #     print(f"{ticker}")
    #     coin_price=get_ticker_price(ticker)
    #     # print(coin_price)
    #     # print(f'{ticker}의 가격은 {coin_price[0]}원입니다')

    while True:
        user_input = input(f"시장 코드를 입력 하세요. 종료 하려면 'q'")
        if user_input =="q":
            break
        if user_input in tickers:
            coin_price = get_ticker_price(user_input)
            print(f"{user_input}의 가격은 {coin_price[0]}원 고가는 {coin_price[1]} 저가는 {coin_price[2]} 변화율은{coin_price[3]*100}% 시가는 {coin_price[4]}")
        else:
            print("유효하지 않은 코드입니다.")

# 사용자가 선택해서 가격을 출력
if __name__ == "__main__":
    main()