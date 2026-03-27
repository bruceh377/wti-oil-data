import yfinance as yf
import pandas as pd
from datetime import datetime
import json
import os

SYMBOL = "CL=F"
OUTPUT_JSON = "wti_data.json"

print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始拉取 WTI 数据...")

ticker = yf.Ticker(SYMBOL)
current_price = ticker.fast_info.get('lastPrice') or ticker.fast_info.get('regularMarketPrice')

df = ticker.history(period="7d", interval="5m")

if df is not None and not df.empty:
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')
    df.reset_index(inplace=True)
    
    df.rename(columns={
        'index': '时间',
        'Open': '开盘',
        'High': '最高',
        'Low': '最低',
        'Close': '收盘',
        'Volume': '成交量'
    }, inplace=True)
    
    for col in ['开盘', '最高', '最低', '收盘']:
        df[col] = df[col].round(2)
    
    data = {
        "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "当前价格": round(float(current_price), 2) if current_price else None,
        "m5_bars": df.tail(50).to_dict(orient='records')
    }
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 更新成功 → 当前价格 {current_price} | 保存 {len(df)} 条 K 线")
else:
    print("⚠️  无数据")
