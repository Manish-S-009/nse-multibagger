import json, datetime
def load_config(path='RUN_CONFIG.json'):
    with open(path) as f:
        cfg = json.load(f)
    if not cfg.get('asof_date_ist'):
        from datetime import datetime, timedelta, tzinfo
        class IST(tzinfo):
            def utcoffset(self, dt): return timedelta(hours=5, minutes=30)
            def tzname(self, dt): return 'IST'
            def dst(self, dt): return timedelta(0)
        cfg['asof_date_ist'] = (datetime.now(IST()) - timedelta(days=1)).strftime('%Y-%m-%d')
    return cfg

def ensure_outputs():
    import os
    os.makedirs('outputs', exist_ok=True)

def save_json(obj,path):
    import json
    with open(path,'w') as f:
        json.dump(obj,f,indent=2,default=str)
