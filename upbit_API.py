import pyupbit
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
    # 총 자산 조회 (현금+총매수금액)
    balances = upbit.get_balances()
    asset = float(balances[0]['balance'])
    for b in balances:
        if b['currency'] != 'KRW':
            asset += float(b['balance'])*float(b['avg_buy_price'])
    return asset


def get_current_price(ticker):
    # 현재가 조회
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def get_ma15(ticker):
    # 15일 이동 평균선 조회
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15
