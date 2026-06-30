import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# 定義要抓取的指標名稱與對應的 Yahoo Finance Ticker
indicators = {
    "美元指數": "DX-Y.NYB",
    "美國-10年期公債殖利率": "^TNX", # 單位為 %
    "道瓊工業指數": "^DJI",
    "S&P 500": "^GSPC",
    "費城半導體指數": "^SOX",
    "那斯達克": "^IXIC",
    "WTI西德州原油": "CL=F",
    "黃金期貨": "GC=F"
}

def fetch_latest_data():
    data_row = {"日期": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    
    for name, ticker in indicators.items():
        try:
            # 抓取過去 5 天的資料以確保能拿到最新收盤價
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            
            if not hist.empty:
                # 取得最後一筆的收盤價，並四捨五入到小數點後兩位
                latest_price = round(hist['Close'].iloc[-1], 2)
                data_row[name] = latest_price
            else:
                data_row[name] = "N/A"
                
        except Exception as e:
            print(f"抓取 {name} ({ticker}) 失敗: {e}")
            data_row[name] = "Error"
            
    return data_row

def save_to_csv(data_row, filename="data.csv"):
    df_new = pd.DataFrame([data_row])
    
    # 檢查檔案是否存在，若不存在則寫入包含標題列的新檔案
    if not os.path.isfile(filename):
        df_new.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"建立新檔案 {filename} 並寫入資料。")
    else:
        # 若存在，則將新資料附加在最下方，不寫入標題列
        df_new.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')
        print(f"資料已成功附加至 {filename}。")

if __name__ == "__main__":
    print("開始抓取市場數據...")
    latest_data = fetch_latest_data()
    print("抓取完成，準備存檔...")
    save_to_csv(latest_data)
