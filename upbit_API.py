import pyupbit
import numpy as np
import time
import datetime

def get_balances(upbit, ticker, value):
    # 종목별 세부항목 조회
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b[value] is not None:
                return float(b[value])
            else:
                return 0
    return 0


def get_asset(upbit):
    # 총 자산 조회 (현금+평가금액)
    balances = upbit.get_balances() # API 1회 호출
    asset_krw = float(balances[0]['balance'])

    currency = []
    balance = []
    for b in balances:
        if b['currency'] != 'KRW':
            currency.append('KRW-'+b['currency'])
            balance.append(b['balance'])

    current_price = pyupbit.get_current_price(currency) # API 1회 호출
    asset_coin = np.dot(list(map(float, balance)), list(map(float, current_price.values())))

    return asset_krw+asset_coin


def get_ma15(ticker):
    # 15일 이동 평균선 조회
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15
