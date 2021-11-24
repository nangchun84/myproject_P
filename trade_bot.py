import os.path

from upbit_API import *
from volatility import *

# upbit API key
with open('upbit-key.txt', 'r') as f :
    access = f.readline().strip()
    secret = f.readline().strip()


# 로그인
upbit = pyupbit.Upbit(access, secret)
print('Trade bot start')

file_name = 'trade_record.xlsx'

if os.path.isfile(file_name):
    record_table = pd.read_excel(file_name, index_col=None)
else:
    record_table = pd.DataFrame({'Name': [], 'DateTime': [], 'Action': [], 'Ticker': [], 'Unit': [], 'Price': []})


# 파라미터 & Input
k = 0.6 # 변동폭 적용계수
fee = 0.0005 # 거래수수료
target_rate = (1.1, 0.9) # 매도 수익률 (상한, 하한)
portfolio_n = 5 # 한번에 보유할 종목 수

asset = get_asset(upbit)


# 종목 선정
tickers = pyupbit.get_tickers(fiat='KRW') # 원화시장 전 종목


# 자동거래 시작
while True:
    try:
        now = datetime.datetime.now()

        # 피드백 시간
        if datetime.datetime(now.year, now.month, now.day, 8, 55, 0) < now < datetime.datetime(now.year, now.month, now.day, 9, 0, 0):

            # 보유종목 모두 매각
            balances = upbit.get_balances()
            for b in balances:
                if b['currency'] != 'KRW':

                    before_krw = get_balances(upbit, 'KRW', 'balance')
                    upbit.sell_market_order('KRW-'+b['currency'], b['balance'])
                    after_krw = get_balances(upbit, 'KRW', 'balance')
                    record_krw = after_krw - before_krw
                    record = pd.DataFrame({'Name': ['VOLT'], 'DateTime': [datetime.datetime.now()], 'Action': ['Sell'],
                                           'Ticker': [ticker], 'Unit': [unit], 'Price': [record_krw / unit]})
                    record_table = record_table.append(record)

                    print(b['currency'], 'sell for end price!')
                    time.sleep(.5)

            record_table.to_excel(file_name, index=False)

            # asset, 종목 업데이트
            asset = get_asset(upbit)
            tickers = pyupbit.get_tickers(fiat='KRW')

        # 일 할 시간
        else:
            for i in tickers:
                print(i, 'trade_VOLT', now)
                record_table = trade_volatility(upbit, i, k, asset / portfolio_n, fee, target_rate, record_table, file_name)
                record_table.to_excel(file_name, index=False)
                time.sleep(.5)

    except Exception as e:
        print(e)
        time.sleep(.5)
