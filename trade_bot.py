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
target_rate = (1.1, 0.9) # 매도 수익률 (상한, 하한)
portfolio_n = 5 # 한번에 보유할 종목 수

global asset
asset = get_asset(upbit)


# 종목 선정
tickers = pyupbit.get_tickers(fiat='KRW')


# 자동거래 시작
while True:
    try:
        for i in tickers:
            print(i, 'trade_volatility', datetime.datetime.now())
            trade_volatility(upbit, i, k, asset/portfolio_n, fee, target_rate)
            time.sleep(.5)

    except Exception as e:
        print(e)
        time.sleep(.5)
