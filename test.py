from upbit_API import *
from volatility import *

# upbit API key
with open('upbit-key.txt', 'r') as f :
    access = f.readline().strip()
    secret = f.readline().strip()


# 로그인
upbit = pyupbit.Upbit(access, secret)
print('Trade bot start')


# 파라미터 & Input
k = 0.6 # 변동폭 적용계수
fee = 0.0005 # 거래수수료
target_rate = 1.1 # 매도 목표수익률
portfolio_n = 5 # 한번에 보유할 종목 수

krw = get_balances(upbit, 'KRW', 'balance')
unit_money = krw / portfolio_n


# 종목 선정
tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-BORA', 'KRW-POWR', 'KRW-HUM', 'KRW-SAND', 'KRW-MANA', 'KRW-MOC', 'KRW-LOOM', 'KRW-POLY']


# 자동거래 시작
while True:
    try:
        for i in tickers:
            trade_volatility(upbit, i, k, unit_money, fee, target_rate)
            print(i, 'trade_volatility', datetime.datetime.now())
            time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)
