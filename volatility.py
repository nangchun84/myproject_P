from upbit_API import *


def v_get_target_price(ticker, k):
    # 변동성돌파전략의 매수목표가격
    df = pyupbit.get_ohlcv(ticker, interval='day', count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


def v_get_start_time(ticker):
    # 시작 시간 조회
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


# 변동성돌파전략 매매 알고리즘
def trade_volatility(upbit, ticker, k, unit_money, fee, target_rate):

    unit = upbit.get_balance(ticker)
    target_price = v_get_target_price(ticker, k)
    ma15 = get_ma15(ticker)
    current_price = pyupbit.get_current_price(ticker)

    # 매수목표가격 돌파 : 매수 or 목표가격 매도
    if target_price < current_price and ma15 < current_price:

        # 보유종목 아니면 매수
        if unit == 0:

            # 돈 있으면삼
            krw = get_balances(upbit, 'KRW', 'balance')
            if krw > unit_money:
                upbit.buy_market_order(ticker, unit_money*(1-fee))
                print(ticker, 'Buy!')

            # 돈 없으면 메시지만
            else:
                print('Not enough money!')

        # 보유종목이면, 목표매도 검사
        else:
            if unit * current_price > 6000: # 이미 목표가격 매도 한번 한 건 놔둠 (6천원 미만 짜리)
                high_price = get_balances(upbit, ticker[4:], 'avg_buy_price') * target_rate[0]  # 목표매도 가격(상한)

                # 보유종목이 목표가격 이상이면 매도
                if high_price <= current_price:
                    upbit.sell_market_order(ticker, unit-5500/current_price) # 목표매도 시, 잔고를 남겨서 또 매매 안하게 (5천원은 남겨야 됨)
                    print(ticker, 'Sell for high price!')

    # 매수목표가격 돌파 아닐 때
    else:

        # 보유종목이면, 손절 검사
        if unit > 0:
            low_price = get_balances(upbit, ticker[4:], 'avg_buy_price') * target_rate[1]  # 손절 기준가격(하한)

            # 보유종목이 손절 기준가격 미만이면 매도
            if low_price > current_price:
                upbit.sell_market_order(ticker, unit)  # 손절했는데 다시 오르면 살 수 있으니, 전량 매도?
                print(ticker, 'sell for minimum price!')