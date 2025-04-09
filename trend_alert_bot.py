import time
import requests
import pandas as pd
import datetime
import telegram

bot_token = '7650426828:AAExcfRRfks8-YDDLLz6R0elDuPk1tw0VzM'
chat_id = '7820787837'
bot = telegram.Bot(token=bot_token)

def get_bitmex_data():
    url = "https://www.bitmex.com/api/v1/trade/bucketed"
    params = {
        "binSize": "5m",
        "symbol": "XBTUSD",
        "count": 100,
        "reverse": True
    }
    response = requests.get(url, params=params)
    return pd.DataFrame(response.json())

def calculate_gann_angle(df):
    df['close_diff'] = df['close'].diff()
    df['gann_angle'] = df['close_diff'].apply(lambda x: round(x, 2))
    return df

def detect_trend_change(df):
    angle = df['gann_angle'].iloc[-1]
    prev_angle = df['gann_angle'].iloc[-2]
    if angle * prev_angle < 0:
        return f"[알림] 추세 전환 감지!\n각도 변화: {prev_angle} → {angle}"
    return None

def main():
    while True:
        try:
            df = get_bitmex_data()
            df = calculate_gann_angle(df)
            alert = detect_trend_change(df)
            if alert:
                bot.send_message(chat_id=chat_id, text=alert)
        except Exception as e:
            bot.send_message(chat_id=chat_id, text=f"[오류 발생] {e}")
        time.sleep(300)

if __name__ == "__main__":
    main()
