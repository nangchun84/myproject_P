from upbit_API import *

def v_get_target_price(ticker, k):
    # 변동성돌파전략의 매수목표가
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
    now = datetime.datetime.now()
    start_time = v_get_start_time(ticker)
    end_time = start_time + datetime.timedelta(days=1)

    # 매수시간
    if start_time < now < end_time - datetime.timedelta(seconds=10):
        target_price = v_get_target_price(ticker, k)
        ma15 = get_ma15(ticker)
        current_price = get_current_price(ticker)

        # 매수목표가 돌파
        if target_price < current_price: # ma15 추가 시, and ma15 < current_price
            krw = get_balances(upbit, 'KRW', 'balance')
            unit = upbit.get_balance(ticker)

            # 기 보유 종목이 아닌경우 매수
            if unit == 0:

                # 돈 있으면 사
                if krw > unit_money:
                    upbit.buy_market_order(ticker, unit_money*(1-fee))
                    print(ticker, '매수')

                else:
                    print('잔고 부족')

            # 보유 종목이면 목표가 매도대상인지 검사
            else:
                if unit * current_price >= 6000:
                    peak_price = get_balances(upbit, ticker[4:], 'avg_buy_price') * target_rate  # 매도 목표가

                    # 보유 종목이 목표가 이상이면 목표가 매도
                    if peak_price <= current_price:
                        upbit.sell_market_order(ticker, unit-5500/current_price) # 목표가 매도 시, 잔고를 남겨서 다시 사지 않게 함
                        print(ticker, '목표가매도')

    # 종가 시간
    else:
        unit = upbit.get_balance(ticker)

        # 보유 종목 모두 매각
        if unit > 0:
            upbit.sell_market_order(ticker, unit)
            print(ticker, '종가매도')
