import pandas as pd
from pathlib import Path
def read_universe(path='symbols/nse_universe.csv'):
    p = Path(path)
    if not p.exists():
        return []
    return [l.strip() for l in p.read_text().splitlines() if l.strip()]

def fetch_prices_yfinance(symbols):
    import yfinance as yf
    import pandas as pd
    dfs = []
    for s in symbols:
        d = yf.download(s, period='5y', interval='1d', auto_adjust=True, progress=False)
        if d is None or d.empty:
            continue
        d = d.reset_index().assign(Symbol=s)
        dfs.append(d)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()
