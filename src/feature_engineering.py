import pandas as pd
def compute_basic_features(prices_df, fund_df, cfg):
    if prices_df.empty:
        return pd.DataFrame()
    prices_df['Date'] = pd.to_datetime(prices_df['Date'])
    rows = []
    for sym, g in prices_df.groupby('Symbol'):
        g = g.sort_values('Date')
        last = g.iloc[-1]
        r1 = None if len(g)<22 else last['Close']/g.iloc[-22]['Close'] - 1
        r6 = None if len(g)<127 else last['Close']/g.iloc[-127]['Close'] - 1
        high12 = g['High'].rolling(window=min(len(g),252)).max().iloc[-1]
        low12 = g['Low'].rolling(window=min(len(g),252)).min().iloc[-1]
        pr = None
        if high12 is not None and low12 is not None and (high12-low12)!=0:
            pr = (last['Close'] - low12)/(high12-low12)*2 - 1
        rows.append({'Symbol':sym,'last_close':last['Close'],'mom1m':r1,'mom6m':r6,'price_range':pr})
    return pd.DataFrame(rows)
