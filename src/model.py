import numpy as np, pandas as pd
from sklearn.linear_model import Ridge

def estimate_system_gmm(panel_df,cfg):
    try:
        from linearmodels.panel import PanelData
        from linearmodels.panel.model import DynamicPanelGMM
        # This demo assumes panel_df has entity/time/many periods. In many cases runner must supply a full panel.
        raise ImportError('GMM path: placeholder - ensure proper panel structure before running DynamicPanelGMM')
    except Exception as e:
        # fallback ridge
        Xcols = ['log_tev','bm','fcfp','roa','ebitda_margin','asset_growth','inv_dummy','mom1m','mom6m','price_range','analyst_coverage']
        for c in Xcols:
            if c not in panel_df.columns:
                panel_df[c]=0.0
        X = panel_df[Xcols].fillna(0).values
        y = panel_df['next_year_return'].fillna(0).values
        model = Ridge(alpha=1.0, random_state=cfg.get('random_seed',42))
        model.fit(X,y)
        coefs = dict(zip(Xcols, model.coef_.tolist()))
        return coefs, {'fallback':'ridge'}

def predict_and_score(latest, coefs, cfg):
    Xcols = list(coefs.keys())
    for c in Xcols:
        if c not in latest.columns:
            latest[c]=0.0
    X = latest[Xcols].fillna(0).values
    preds = X.dot(np.array([coefs[c] for c in Xcols]))
    latest['pred_1y']=preds
    latest['pred_cagr'] = (1+latest['pred_1y']).clip(lower=-0.9)**(1/4)-1
    latest['Predicted CAGR (%)'] = (latest['pred_cagr']*100).round(2)
    return latest.sort_values('Predicted CAGR (%)', ascending=False)
