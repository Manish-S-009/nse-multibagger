from src.utils import load_config, ensure_outputs, save_json
from src.fetch_data import read_universe, fetch_prices_yfinance
from src.feature_engineering import compute_basic_features
from src.model import estimate_system_gmm, predict_and_score
import numpy as np

def main():
    cfg = load_config('../RUN_CONFIG.json')
    ensure_outputs()
    universe = read_universe('../symbols/nse_universe.csv')
    print('Universe', len(universe))
    prices = fetch_prices_yfinance(universe)
    funds = None
    features = compute_basic_features(prices, funds, cfg)
    # Add synthetic fields for demo
    features['next_year_return'] = np.random.normal(0.1,0.2,size=len(features))
    # supply common regressors with defaults
    for c in ['log_tev','bm','fcfp','roa','ebitda_margin','asset_growth','inv_dummy','analyst_coverage']:
        if c not in features.columns:
            features[c]=0.0
    coefs, diag = estimate_system_gmm(features, cfg)
    save_json({'coefs':coefs,'diag':diag}, 'outputs/model_fit.json')
    latest = features
    scored = predict_and_score(latest, coefs, cfg)
    scored[['Symbol','Predicted CAGR (%)']].to_csv('outputs/top50_multibaggers_Tminus1.csv', index=False)
    save_json({'asof': cfg['asof_date_ist']}, 'outputs/run_provenance.json')
    print('Done. outputs written to outputs/')


if __name__=='__main__':
    main()
