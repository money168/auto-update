import yfinance as yf
import pandas as pd
from datetime import datetime
import os

indicators = {
    "美元指數": "DX-Y.NYB",
    "美國-10年期公債殖利率": "^TNX",
    "道瓊工業指數": "^DJI",
    "S&P 500": "^GSPC",
    "費城半導體指數": "^SOX",
    "那斯達克": "^IXIC",
    "WTI西德州原油": "CL=F",
    "黃金期貨": "GC=F"
}

def fetch_latest_data():
    # 取得當下時間
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_row = {"日期": current_time}
    
    # 準備用來發送給 Teams 的摘要文字
    summary_lines = [f"🕒 **更新時間**: {current_time}", ""]
    
    for name, ticker in indicators.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            
            if not hist.empty:
                latest_price = round(hist['Close'].iloc[-1], 2)
                data_row[name] = latest_price
                # 將最新報價加入摘要中
                summary_lines.append(f"- **{name}**: {latest_price}")
            else:
                data_row[name] = "N/A"
                summary_lines.append(f"- **{name}**: N/A")
                
        except Exception as e:
            print(f"抓取 {name} ({ticker}) 失敗: {e}")
            data_row[name] = "Error"
            summary_lines.append(f"- **{name}**: Error")
            
    # 將摘要寫入純文字檔，供後續 GitHub Actions 讀取發送
    with open("latest_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))
        print("已產生 Teams 訊息摘要檔 (latest_summary.txt)。")
        
    return data_row

def save_to_csv(data_row, filename="data.csv"):
    df_new = pd.DataFrame([data_row])
    
    if not os.path.isfile(filename):
        df_new.to_csv(filename, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    print("開始抓取市場數據...")
    latest_data = fetch_latest_data()
    save_to_csv(latest_data)
    print("數據處理完畢。")
