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
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_row = {"日期": current_time}
    
    summary_lines = [f"🕒 **更新時間**: {current_time}", ""]
    
    for name, ticker in indicators.items():
        try:
            stock = yf.Ticker(ticker)
            # 抓取過去 5 天資料，確保即使遇到假日也能拿到最近「兩個交易日」的數據
            hist = stock.history(period="5d")
            
            if len(hist) >= 2:
                # 取得最新收盤價與前一日收盤價
                latest_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                
                # 計算漲跌點數與漲跌幅
                change = latest_price - prev_price
                pct_change = (change / prev_price) * 100
                
                # 判斷趨勢並給予對應的符號
                if change > 0:
                    emoji = "🔺"
                elif change < 0:
                    emoji = "🔻"
                else:
                    emoji = "➖"
                
                # 將資料寫入 CSV 專用的字典中 (擴充欄位)
                data_row[f"{name}_報價"] = round(latest_price, 2)
                data_row[f"{name}_漲跌"] = round(change, 2)
                data_row[f"{name}_幅(%)"] = round(pct_change, 2)
                
                # 寫入 Teams 推播摘要 (使用 :+.2f 強制顯示正負號並取小數點後兩位)
                summary_lines.append(f"- **{name}**: {latest_price:.2f} ({emoji} {change:+.2f} / {pct_change:+.2f}%)")
                
            else:
                data_row[f"{name}_報價"] = "N/A"
                data_row[f"{name}_漲跌"] = "N/A"
                data_row[f"{name}_幅(%)"] = "N/A"
                summary_lines.append(f"- **{name}**: 資料不足無法計算")
                
        except Exception as e:
            print(f"抓取 {name} ({ticker}) 失敗: {e}")
            data_row[f"{name}_報價"] = "Error"
            data_row[f"{name}_漲跌"] = "Error"
            data_row[f"{name}_幅(%)"] = "Error"
            summary_lines.append(f"- **{name}**: 抓取失敗")
            
    with open("latest_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))
        print("已產生包含漲跌資訊的 Teams 訊息摘要檔。")
        
    return data_row

def save_to_csv(data_row, filename="data.csv"):
    df_new = pd.DataFrame([data_row])
    
    if not os.path.isfile(filename):
        df_new.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"建立新檔案 {filename} 並寫入資料。")
    else:
        df_new.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')
        print(f"資料已成功附加至 {filename}。")

if __name__ == "__main__":
    print("開始抓取市場數據...")
    latest_data = fetch_latest_data()
    save_to_csv(latest_data)
    print("數據處理完畢。")
