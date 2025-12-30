"""
Predictive Analysis Module
Dengue Surveillance System - Zamboanga Sibugay
Using Negative Binomial (NB) and Zero-Inflated Negative Binomial (ZINB) Regression
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.append('..')

try:
    from styles import SHARED_CSS, render_header, render_section_header, render_footer, render_sidebar_header, render_info_box
except:
    from styles import SHARED_CSS, render_header, render_section_header, render_footer, render_sidebar_header, render_info_box

# Try imports for models
try:
    import statsmodels.api as sm
    from statsmodels.discrete.count_model import ZeroInflatedNegativeBinomialP
    from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
    STATSMODELS_AVAILABLE = True
    MARKOV_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    MARKOV_AVAILABLE = False

# Try imports for mapping
try:
    import geopandas as gpd
    from shapely import wkt
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False

# Apply shared styles
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# Additional custom styles
st.markdown("""
<style>
    .pred-card {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(16, 185, 129, 0.3);
        margin-bottom: 1rem;
    }
    .pred-card.high { background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); box-shadow: 0 10px 40px rgba(239, 68, 68, 0.3); }
    .pred-card.medium { background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); box-shadow: 0 10px 40px rgba(245, 158, 11, 0.3); }
    .pred-card.low { background: linear-gradient(135deg, #10B981 0%, #059669 100%); box-shadow: 0 10px 40px rgba(16, 185, 129, 0.3); }
    .pred-value { font-size: 3.5rem; font-weight: 800; line-height: 1; }
    .pred-label { font-size: 1rem; opacity: 0.9; margin-top: 0.5rem; }
    .pred-sublabel { font-size: 0.85rem; opacity: 0.8; margin-top: 0.25rem; }
    .pred-badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-top: 0.75rem; }
    .perf-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.75rem; margin: 1rem 0; }
    .perf-item { background: #F9FAFB; padding: 1rem; border-radius: 8px; text-align: center; border: 1px solid #E5E7EB; }
    .perf-item .val { font-size: 1.25rem; font-weight: 700; color: #1F2937; }
    .perf-item .lbl { font-size: 0.7rem; color: #6B7280; font-weight: 500; margin-top: 0.25rem; }
    .sig-positive { color: #059669; font-weight: 600; }
    .sig-negative { color: #DC2626; font-weight: 600; }
    .sig-neutral { color: #6B7280; }
    .risk-critical { background: #FEE2E2; color: #991B1B; }
    .risk-high { background: #FFEDD5; color: #9A3412; }
    .risk-moderate { background: #FEF3C7; color: #92400E; }
    .risk-low { background: #D1FAE5; color: #065F46; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('sibugay_dengue_cases_dataset.csv')
        return df
    except FileNotFoundError:
        return None

def find_columns(df):
    """Dynamically find relevant columns"""
    columns = {}
    col_lower = {c.lower(): c for c in df.columns}
    
    for pattern in ['mun', 'municipality', 'city', 'location']:
        for key, orig in col_lower.items():
            if pattern in key:
                columns['location'] = orig
                break
        if 'location' in columns:
            break
    
    for pattern in ['case', 'count', 'total']:
        for key, orig in col_lower.items():
            if pattern in key and 'date' not in key:
                columns['cases'] = orig
                break
        if 'cases' in columns:
            break
    
    for pattern in ['year_2', 'year']:
        for key, orig in col_lower.items():
            if pattern in key:
                columns['year'] = orig
                break
        if 'year' in columns:
            break
    
    for pattern in ['morbidity_week', 'morbidity']:
        for key, orig in col_lower.items():
            if pattern in key:
                columns['week'] = orig
                break
        if 'week' in columns:
            break
    
    if 'week' not in columns:
        for key, orig in col_lower.items():
            if 'week' in key and 'year' not in key and df[orig].nunique() > 1:
                columns['week'] = orig
                break
    
    for pattern in ['geometry', 'geom']:
        for key, orig in col_lower.items():
            if pattern in key:
                columns['geometry'] = orig
                break
        if 'geometry' in columns:
            break
    
    # Environmental columns
    for pattern in ['t2m_max', 'temp_max', 'temperature']:
        for key, orig in col_lower.items():
            if pattern in key:
                columns['temp_max'] = orig
                break
        if 'temp_max' in columns:
            break
    
    for pattern in ['rh2m', 'humidity', 'rh']:
        for key, orig in col_lower.items():
            if pattern in key:
                columns['humidity'] = orig
                break
        if 'humidity' in columns:
            break
    
    for pattern in ['prectot', 'precip', 'rain']:
        for key, orig in col_lower.items():
            if pattern in key:
                columns['precipitation'] = orig
                break
        if 'precipitation' in columns:
            break
    
    return columns

def get_dataset_dates(df, year_col, week_col):
    """Get last date in dataset"""
    # Drop NaN values before converting
    clean_df = df.dropna(subset=[year_col, week_col])
    years = clean_df[year_col].astype(int)
    max_year = years.max()
    full_year = 2000 + max_year if max_year < 100 else max_year
    
    max_year_data = clean_df[clean_df[year_col].astype(int) == max_year]
    max_week = int(max_year_data[week_col].max())
    
    jan1 = datetime(full_year, 1, 1)
    if jan1.weekday() <= 3:
        week1_start = jan1 - timedelta(days=jan1.weekday())
    else:
        week1_start = jan1 + timedelta(days=7 - jan1.weekday())
    
    last_date = week1_start + timedelta(weeks=max_week - 1)
    return last_date, full_year, max_week

def prepare_regression_data(df, cols):
    """Prepare time series for regression"""
    time_series = df.groupby([cols['year'], cols['week']])[cols['cases']].sum().reset_index()
    time_series.columns = ['year', 'week', 'cases']
    time_series = time_series.sort_values(['year', 'week']).reset_index(drop=True)
    time_series['time_index'] = range(len(time_series))
    time_series['lag1'] = time_series['cases'].shift(1).fillna(0)
    time_series['rolling_mean_4'] = time_series['cases'].rolling(window=4, min_periods=1).mean()
    
    for col in ['cases', 'time_index', 'lag1', 'rolling_mean_4']:
        time_series[col] = time_series[col].astype(float)
    
    return time_series

def prepare_full_regression_data(df, cols):
    """Prepare data with environmental variables for significance analysis"""
    # Aggregate by time period
    agg_dict = {cols['cases']: 'sum'}
    
    if 'temp_max' in cols:
        agg_dict[cols['temp_max']] = 'mean'
    if 'humidity' in cols:
        agg_dict[cols['humidity']] = 'mean'
    if 'precipitation' in cols:
        agg_dict[cols['precipitation']] = 'mean'
    
    time_series = df.groupby([cols['year'], cols['week']]).agg(agg_dict).reset_index()
    
    # Rename columns
    rename_dict = {cols['year']: 'year', cols['week']: 'week', cols['cases']: 'cases'}
    if 'temp_max' in cols:
        rename_dict[cols['temp_max']] = 'temp_max'
    if 'humidity' in cols:
        rename_dict[cols['humidity']] = 'humidity'
    if 'precipitation' in cols:
        rename_dict[cols['precipitation']] = 'precipitation'
    
    time_series = time_series.rename(columns=rename_dict)
    time_series = time_series.sort_values(['year', 'week']).reset_index(drop=True)
    
    # Add features
    time_series['time_index'] = range(len(time_series))
    time_series['lag1'] = time_series['cases'].shift(1).fillna(0)
    time_series['lag2'] = time_series['cases'].shift(2).fillna(0)
    time_series['rolling_mean_4'] = time_series['cases'].rolling(window=4, min_periods=1).mean()
    
    # Convert to float
    for col in time_series.columns:
        if col not in ['year', 'week']:
            time_series[col] = time_series[col].astype(float)
    
    return time_series

def fit_negative_binomial(train_data):
    """Fit NB model"""
    if not STATSMODELS_AVAILABLE:
        return None, None
    try:
        X = train_data[['time_index', 'lag1', 'rolling_mean_4']].values.astype(float)
        X = sm.add_constant(X, has_constant='add')
        y = train_data['cases'].values.astype(float)
        model = sm.GLM(y, X, family=sm.families.NegativeBinomial(alpha=1.0))
        results = model.fit(disp=0)
        return model, results
    except:
        return None, None

def fit_nb_with_env(train_data):
    """Fit NB model with environmental variables for significance analysis"""
    if not STATSMODELS_AVAILABLE:
        return None, None
    
    try:
        # Build feature list
        feature_cols = ['time_index', 'lag1', 'rolling_mean_4']
        feature_names = ['Time Trend', 'Previous Week Cases', '4-Week Rolling Average']
        
        if 'temp_max' in train_data.columns:
            feature_cols.append('temp_max')
            feature_names.append('Max Temperature')
        if 'humidity' in train_data.columns:
            feature_cols.append('humidity')
            feature_names.append('Humidity')
        if 'precipitation' in train_data.columns:
            feature_cols.append('precipitation')
            feature_names.append('Precipitation')
        
        X = train_data[feature_cols].values.astype(float)
        X = sm.add_constant(X, has_constant='add')
        y = train_data['cases'].values.astype(float)
        
        model = sm.GLM(y, X, family=sm.families.NegativeBinomial(alpha=1.0))
        results = model.fit(disp=0)
        
        return results, ['Intercept'] + feature_names
    except:
        return None, None

def fit_zinb(train_data):
    """Fit ZINB model"""
    if not STATSMODELS_AVAILABLE:
        return None, None
    try:
        X = train_data[['time_index', 'lag1', 'rolling_mean_4']].values.astype(float)
        X = sm.add_constant(X, has_constant='add')
        y = train_data['cases'].values.astype(float)
        X_infl = np.ones((len(y), 1))
        model = ZeroInflatedNegativeBinomialP(y, X, exog_infl=X_infl)
        results = model.fit(disp=0, maxiter=300, method='bfgs')
        return model, results
    except:
        try:
            X_simple = sm.add_constant(train_data[['lag1']].values.astype(float))
            y = train_data['cases'].values.astype(float)
            X_infl = np.ones((len(y), 1))
            model = ZeroInflatedNegativeBinomialP(y, X_simple, exog_infl=X_infl)
            results = model.fit(disp=0, maxiter=300, method='nm')
            return model, results
        except:
            return None, None

def fit_markov_switching_nb(train_data):
    """Fit Markov-Switching Negative Binomial model"""
    if not MARKOV_AVAILABLE:
        print("Markov not available")
        return None, None
    try:
        # Prepare exogenous variables - simpler approach
        y = train_data['cases'].values.astype(float)
        X = train_data[['lag1']].values.astype(float)
        
        # Fit Markov-switching model with 2 regimes (low/high outbreak states)
        model = MarkovRegression(
            endog=y,
            k_regimes=2,
            exog=X,
            switching_variance=True
        )
        results = model.fit(maxiter=200, disp=False, warn_convergence=False)
        print(f"Markov model fitted successfully. AIC: {results.aic:.2f}")
        return model, results
    except Exception as e:
        print(f"Markov fitting error (first attempt): {str(e)[:100]}")
        # Fallback to even simpler specification
        try:
            y = train_data['cases'].values.astype(float)
            # Just use constant term, no exog variables
            model = MarkovRegression(
                endog=y,
                k_regimes=2,
                switching_variance=False
            )
            results = model.fit(maxiter=200, disp=False, warn_convergence=False)
            print(f"Markov model fitted (simple). AIC: {results.aic:.2f}")
            return model, results
        except Exception as e2:
            print(f"Markov fitting error (fallback): {str(e2)[:100]}")
            return None, None

def predict_with_model(results, test_data, model_type='nb'):
    """Make predictions"""
    try:
        if model_type == 'zinb':
            n_params = results.model.exog.shape[1]
            if n_params == 4:
                X_test = test_data[['time_index', 'lag1', 'rolling_mean_4']].values.astype(float)
            else:
                X_test = test_data[['lag1']].values.astype(float)
            X_test = sm.add_constant(X_test, has_constant='add')
            predictions = results.predict(X_test, exog_infl=np.ones((len(test_data), 1)))
        elif model_type == 'markov':
            # For Markov-switching, use expected value across regimes
            try:
                if results.model.exog is not None:
                    X_test = test_data[['lag1']].values.astype(float)
                    predictions = results.predict(exog=X_test)
                else:
                    # No exog variables - just predict based on fitted model
                    predictions = results.predict()
                    # Extend to test data length if needed
                    if len(predictions) < len(test_data):
                        predictions = np.tile(predictions.mean(), len(test_data))
            except Exception as e:
                print(f"Markov prediction error: {str(e)[:100]}")
                predictions = results.predict()
        else:
            X_test = test_data[['time_index', 'lag1', 'rolling_mean_4']].values.astype(float)
            X_test = sm.add_constant(X_test, has_constant='add')
            predictions = results.predict(X_test)
        return np.array(predictions).flatten()
    except:
        return None

def calculate_metrics(actual, predicted):
    """Calculate performance metrics"""
    actual = np.array(actual).flatten().astype(float)
    predicted = np.array(predicted).flatten().astype(float)
    
    mse = np.mean((actual - predicted) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(actual - predicted))
    
    naive_errors = np.abs(np.diff(actual))
    mase = mae / np.mean(naive_errors) if len(naive_errors) > 0 and np.mean(naive_errors) > 0 else np.nan
    
    tolerance = 0.2
    within_tolerance = np.abs(actual - predicted) <= (tolerance * np.maximum(actual, 1))
    accuracy = np.mean(within_tolerance) * 100
    
    return {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'MASE': mase, 'Accuracy': accuracy}

def calculate_aic_bic(results, n_obs, model_type='nb'):
    """
    Calculate AIC and BIC for model comparison
    
    AIC = 2k - 2ln(L)
    BIC = k*ln(n) - 2ln(L)
    
    where:
    - k = number of parameters
    - L = likelihood
    - n = number of observations
    """
    try:
        if hasattr(results, 'aic') and hasattr(results, 'bic'):
            # Model already has AIC/BIC computed
            aic = float(results.aic)
            bic = float(results.bic)
        else:
            # Calculate manually
            k = len(results.params)  # number of parameters
            log_likelihood = float(results.llf)  # log-likelihood
            
            aic = 2 * k - 2 * log_likelihood
            bic = k * np.log(n_obs) - 2 * log_likelihood
        
        return {'AIC': aic, 'BIC': bic}
    except Exception as e:
        return {'AIC': np.nan, 'BIC': np.nan}

def predict_future(results, last_data, weeks_ahead=4, model_type='nb'):
    """Predict future cases"""
    predictions = []
    current_lag1 = float(last_data['cases'].iloc[-1])
    current_rolling = float(last_data['rolling_mean_4'].iloc[-1])
    next_time_index = float(last_data['time_index'].iloc[-1]) + 1
    
    for i in range(weeks_ahead):
        if model_type == 'zinb':
            try:
                n_params = results.model.exog.shape[1]
                if n_params == 4:
                    X_future = np.array([[1.0, next_time_index + i, current_lag1, current_rolling]])
                else:
                    X_future = np.array([[1.0, current_lag1]])
                pred = results.predict(X_future, exog_infl=np.ones((1, 1)))
            except:
                pred = [current_rolling]
        elif model_type == 'markov':
            try:
                if results.model.exog is not None:
                    X_future = np.array([[current_lag1]])
                    pred = results.predict(exog=X_future)
                    if hasattr(pred, '__iter__'):
                        pred_value = float(pred[-1] if len(pred) > 0 else current_rolling)
                    else:
                        pred_value = float(pred)
                else:
                    # No exog - use smoothed predicted mean
                    pred_value = results.smoothed_marginal_probabilities[:, 0].mean() * results.params[0] + \
                                 results.smoothed_marginal_probabilities[:, 1].mean() * results.params[1]
                pred = [pred_value]
            except Exception as e:
                print(f"Markov future prediction error: {str(e)[:100]}")
                pred = [current_rolling]
        else:
            X_future = np.array([[1.0, next_time_index + i, current_lag1, current_rolling]])
            try:
                pred = results.predict(X_future)
            except:
                pred = [current_rolling]
        
        pred_value = float(np.array(pred).flatten()[0])
        predictions.append(max(0, pred_value))
        current_lag1 = pred_value
        current_rolling = (current_rolling * 3 + pred_value) / 4
    
    return predictions

def calculate_municipality_risk(df, cols, selected_year=None, selected_weeks=4):
    """Calculate risk by municipality with filters"""
    if selected_year is None or selected_year == 'All Years':
        # Use all data when "All Years" is selected
        if selected_year == 'All Years':
            recent_data = df.copy()
            max_week = df[cols['week']].max()
        else:
            max_year = df[cols['year']].max()
            recent_data = df[df[cols['year']] == max_year]
            max_week = recent_data[cols['week']].max()
    else:
        max_year = selected_year
        recent_data = df[df[cols['year']] == max_year]
        max_week = recent_data[cols['week']].max()
    
    # For "All Years", aggregate all data; otherwise filter by recent weeks
    if selected_year == 'All Years':
        recent_weeks = recent_data
    else:
        recent_weeks = recent_data[recent_data[cols['week']] >= max(1, max_week - selected_weeks + 1)]
    
    risk_df = recent_weeks.groupby(cols['location']).agg({
        cols['cases']: ['sum', 'mean', 'max', 'std']
    }).reset_index()
    risk_df.columns = ['municipality', 'total_cases', 'avg_cases', 'max_cases', 'std_cases']
    risk_df['std_cases'] = risk_df['std_cases'].fillna(0)
    
    # Calculate risk score
    if risk_df['total_cases'].max() > 0:
        risk_df['risk_score'] = (risk_df['total_cases'] / risk_df['total_cases'].max() * 100).round(1)
    else:
        risk_df['risk_score'] = 0
    
    # Categorize risk
    risk_df['risk_level'] = pd.cut(
        risk_df['risk_score'],
        bins=[-1, 25, 50, 75, 100],
        labels=['Low', 'Moderate', 'High', 'Critical']
    )
    
    # Calculate trend (using std as volatility indicator)
    risk_df['trend'] = risk_df.apply(
        lambda x: '↑ Increasing' if x['std_cases'] > x['avg_cases'] * 0.5 else 
                  ('↓ Stable' if x['avg_cases'] < 1 else '→ Steady'),
        axis=1
    )
    
    return risk_df.sort_values('risk_score', ascending=False)

# Main Application
def main():
    # Load data
    df = load_data()
    if df is None:
        st.error("Dataset not found.")
        return
    
    cols = find_columns(df)
    required = ['location', 'cases', 'year', 'week']
    missing = [r for r in required if r not in cols]
    if missing:
        st.error(f"Missing columns: {missing}")
        return
    
    # Get dates and prepare data
    last_date, last_year, last_week = get_dataset_dates(df, cols['year'], cols['week'])
    time_series = prepare_regression_data(df, cols)
    full_time_series = prepare_full_regression_data(df, cols)
    
    train_size = int(len(time_series) * 0.8)
    train_data = time_series.iloc[:train_size].copy()
    test_data = time_series.iloc[train_size:].copy()
    
    # Sidebar
    with st.sidebar:
        st.markdown(render_sidebar_header(), unsafe_allow_html=True)
        
        st.markdown("### Forecast Settings")
        forecast_weeks = st.slider("Forecast Weeks", 1, 8, 4)
        
        st.markdown("---")
        st.markdown("### Map Filters")
        
        # Year selection for map
        available_years = sorted(df[cols['year']].unique())
        year_options = ['All Years'] + list(available_years)
        year_labels = {y: f"20{int(y)}" if y != 'All Years' else 'All Years' for y in year_options}
        selected_year = st.selectbox(
            "Select Year",
            year_options,
            index=0,  # Default to "All Years"
            format_func=lambda x: year_labels[x]
        )
        
        # Weeks to analyze - only show when specific year is selected
        if selected_year != 'All Years':
            weeks_window = st.slider("Analysis Window (weeks)", 1, 52, 4)
        else:
            weeks_window = 52  # Use all weeks when "All Years" is selected
            st.markdown("*Showing all available data*")
        
        st.markdown("---")
        st.markdown("**Models:**")
        st.markdown("• Negative Binomial")
        st.markdown("• Zero-Inflated NB")
        st.markdown("• Markov-Switching NB")
    
    # Header
    st.markdown(render_header(
        title="Predictive Analysis",
        subtitle="Forecasting dengue outbreaks using NB and ZINB regression models",
        badge="Machine Learning"
    ), unsafe_allow_html=True)
    
    # Info box
    next_week_date = last_date + timedelta(weeks=1)
    next_week_num = last_week + 1 if last_week < 52 else 1
    next_week_year = last_year if last_week < 52 else last_year + 1
    
    st.markdown(f"""
    <div class="info-box">
        <strong>Forecast Period:</strong> Week {next_week_num}, {next_week_year} 
        ({next_week_date.strftime('%B %d, %Y')})<br>
        <strong>Data through:</strong> Week {last_week}, {last_year} 
        ({last_date.strftime('%B %d, %Y')})
    </div>
    """, unsafe_allow_html=True)
    
    # Fit models
    nb_model, nb_results = fit_negative_binomial(time_series)
    zinb_model, zinb_results = fit_zinb(time_series)
    markov_model, markov_results = fit_markov_switching_nb(time_series)
    
    # Debug: Show model status
    models_status = []
    if nb_results: models_status.append("✓ NB")
    if zinb_results: models_status.append("✓ ZINB")
    if markov_results: models_status.append("✓ Markov")
    
    if models_status:
        st.info(f"Models loaded: {' | '.join(models_status)}")
    
    # Predictions Section
    st.markdown(render_section_header("Next Week Forecast"), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    recent_avg = float(time_series['cases'].tail(4).mean())
    
    with col1:
        if nb_results:
            nb_pred = predict_future(nb_results, time_series, forecast_weeks, 'nb')
            nb_next = round(nb_pred[0], 1)
            risk_class = "high" if nb_next > recent_avg * 1.5 else "medium" if nb_next > recent_avg else "low"
            risk_text = "HIGH RISK" if risk_class == "high" else "MODERATE" if risk_class == "medium" else "LOW RISK"
            
            st.markdown(f"""
            <div class="pred-card {risk_class}">
                <div class="pred-label">Negative Binomial Model</div>
                <div class="pred-value">{nb_next}</div>
                <div class="pred-sublabel">Predicted Cases - Week {next_week_num}</div>
                <div class="pred-badge">{risk_text}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("NB model unavailable")
    
    with col2:
        if zinb_results:
            zinb_pred = predict_future(zinb_results, time_series, forecast_weeks, 'zinb')
            zinb_next = round(zinb_pred[0], 1)
            risk_class = "high" if zinb_next > recent_avg * 1.5 else "medium" if zinb_next > recent_avg else "low"
            risk_text = "HIGH RISK" if risk_class == "high" else "MODERATE" if risk_class == "medium" else "LOW RISK"
            
            st.markdown(f"""
            <div class="pred-card {risk_class}">
                <div class="pred-label">Zero-Inflated NB Model</div>
                <div class="pred-value">{zinb_next}</div>
                <div class="pred-sublabel">Predicted Cases - Week {next_week_num}</div>
                <div class="pred-badge">{risk_text}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("ZINB model unavailable")
    
    with col3:
        if markov_results:
            markov_pred = predict_future(markov_results, time_series, forecast_weeks, 'markov')
            markov_next = round(markov_pred[0], 1)
            risk_class = "high" if markov_next > recent_avg * 1.5 else "medium" if markov_next > recent_avg else "low"
            risk_text = "HIGH RISK" if risk_class == "high" else "MODERATE" if risk_class == "medium" else "LOW RISK"
            
            st.markdown(f"""
            <div class="pred-card {risk_class}">
                <div class="pred-label">Markov-Switching NB</div>
                <div class="pred-value">{markov_next}</div>
                <div class="pred-sublabel">Predicted Cases - Week {next_week_num}</div>
                <div class="pred-badge">{risk_text}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Markov model unavailable")
    
    # Forecast Chart
    st.markdown(render_section_header(f"{forecast_weeks}-Week Forecast"), unsafe_allow_html=True)
    
    fig_forecast = go.Figure()
    historical = time_series.tail(16)
    
    fig_forecast.add_trace(go.Scatter(
        x=list(range(len(historical))),
        y=historical['cases'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#1F2937', width=2),
        marker=dict(size=6)
    ))
    
    if nb_results:
        fig_forecast.add_trace(go.Scatter(
            x=list(range(len(historical), len(historical) + forecast_weeks)),
            y=nb_pred,
            mode='lines+markers',
            name='NB Forecast',
            line=dict(color='#667eea', width=2, dash='dash'),
            marker=dict(size=8, symbol='diamond')
        ))
    
    if zinb_results:
        fig_forecast.add_trace(go.Scatter(
            x=list(range(len(historical), len(historical) + forecast_weeks)),
            y=zinb_pred,
            mode='lines+markers',
            name='ZINB Forecast',
            line=dict(color='#10B981', width=2, dash='dot'),
            marker=dict(size=8, symbol='square')
        ))
    
    if markov_results:
        fig_forecast.add_trace(go.Scatter(
            x=list(range(len(historical), len(historical) + forecast_weeks)),
            y=markov_pred,
            mode='lines+markers',
            name='Markov Forecast',
            line=dict(color='#F59E0B', width=2, dash='dashdot'),
            marker=dict(size=8, symbol='star')
        ))
    
    fig_forecast.update_layout(
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title="Time Period",
        yaxis_title="Cases",
        margin=dict(t=40)
    )
    fig_forecast.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig_forecast.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Forecast Table
    forecast_table = []
    for i in range(forecast_weeks):
        week_num = (last_week + i + 1) if (last_week + i + 1) <= 52 else (last_week + i + 1 - 52)
        year_num = last_year if (last_week + i + 1) <= 52 else last_year + 1
        forecast_table.append({
            'Period': f"Week {week_num}, {year_num}",
            'Date': (last_date + timedelta(weeks=i+1)).strftime('%b %d, %Y'),
            'NB Prediction': round(nb_pred[i], 1) if nb_results else '-',
            'ZINB Prediction': round(zinb_pred[i], 1) if zinb_results else '-',
            'Markov Prediction': round(markov_pred[i], 1) if markov_results else '-'
        })
    
    st.dataframe(pd.DataFrame(forecast_table), use_container_width=True, hide_index=True)
    
    # Interactive Risk Map
    year_display = "All Years" if selected_year == 'All Years' else f"Year 20{int(selected_year)}"
    window_display = "" if selected_year == 'All Years' else f" (Last {weeks_window} Weeks)"
    st.markdown(render_section_header(f"Risk Map - {year_display}{window_display}"), unsafe_allow_html=True)
    
    risk_df = calculate_municipality_risk(df, cols, selected_year, weeks_window)
    geometry_col = cols.get('geometry')
    
    if GEOPANDAS_AVAILABLE and geometry_col:
        try:
            muni_geo = df.drop_duplicates(subset=[cols['location']])[[cols['location'], geometry_col]].copy()
            muni_geo.columns = ['municipality', 'geometry']
            map_data = risk_df.merge(muni_geo, on='municipality', how='left')
            
            geometries = map_data['geometry'].apply(lambda x: wkt.loads(x) if pd.notna(x) else None)
            gdf = gpd.GeoDataFrame(map_data, geometry=geometries, crs="EPSG:4326")
            gdf['centroid'] = gdf.geometry.centroid
            gdf['lon'] = gdf['centroid'].x
            gdf['lat'] = gdf['centroid'].y
            
            fig_map = px.choropleth_mapbox(
                gdf,
                geojson=gdf.geometry.__geo_interface__,
                locations=gdf.index,
                color='risk_score',
                color_continuous_scale='RdYlGn_r',
                range_color=[0, 100],
                mapbox_style='carto-positron',
                center={'lat': gdf['lat'].mean(), 'lon': gdf['lon'].mean()},
                zoom=8,
                opacity=0.75,
                hover_name='municipality',
                hover_data={
                    'risk_score': ':.1f',
                    'total_cases': True,
                    'avg_cases': ':.1f',
                    'risk_level': True
                },
                labels={
                    'risk_score': 'Risk Score',
                    'total_cases': 'Total Cases',
                    'avg_cases': 'Avg Cases/Week',
                    'risk_level': 'Risk Level'
                }
            )
            fig_map.update_layout(
                height=450,
                margin=dict(l=0, r=0, t=0, b=0),
                coloraxis_colorbar=dict(
                    title='Risk',
                    tickvals=[0, 25, 50, 75, 100],
                    ticktext=['Low', '', 'Mod', '', 'Critical']
                )
            )
            st.plotly_chart(fig_map, use_container_width=True)
        except Exception as e:
            st.warning(f"Map error: {e}")
    
    # Risk Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        critical_count = len(risk_df[risk_df['risk_level'] == 'Critical'])
        st.metric("Critical Risk", critical_count, delta="municipalities")
    with col2:
        high_count = len(risk_df[risk_df['risk_level'] == 'High'])
        st.metric("High Risk", high_count, delta="municipalities")
    with col3:
        mod_count = len(risk_df[risk_df['risk_level'] == 'Moderate'])
        st.metric("Moderate Risk", mod_count, delta="municipalities")
    with col4:
        low_count = len(risk_df[risk_df['risk_level'] == 'Low'])
        st.metric("Low Risk", low_count, delta="municipalities")
    
    # Municipality Risk Table
    st.markdown(render_section_header("Municipalities at Risk"), unsafe_allow_html=True)
    
    if selected_year == 'All Years':
        st.markdown(f"""
        <div class="info-box">
            Showing risk assessment for <strong>All Years</strong> (cumulative data). 
            Adjust filters in the sidebar to view specific years.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="info-box">
            Showing risk assessment for <strong>Year 20{int(selected_year)}</strong> based on the 
            last <strong>{weeks_window} weeks</strong> of data. Adjust filters in the sidebar to update.
        </div>
        """, unsafe_allow_html=True)
    
    # Format the risk table
    display_df = risk_df[['municipality', 'total_cases', 'avg_cases', 'max_cases', 'risk_score', 'risk_level', 'trend']].copy()
    display_df.columns = ['Municipality', 'Total Cases', 'Avg/Week', 'Peak', 'Risk Score', 'Risk Level', 'Trend']
    display_df['Avg/Week'] = display_df['Avg/Week'].round(1)
    display_df['Risk Score'] = display_df['Risk Score'].round(1)
    
    # Style the dataframe
    def highlight_risk(row):
        if row['Risk Level'] == 'Critical':
            return ['background-color: #FEE2E2'] * len(row)
        elif row['Risk Level'] == 'High':
            return ['background-color: #FFEDD5'] * len(row)
        elif row['Risk Level'] == 'Moderate':
            return ['background-color: #FEF3C7'] * len(row)
        else:
            return ['background-color: #D1FAE5'] * len(row)
    
    styled_df = display_df.style.apply(highlight_risk, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Top Risk Municipalities
    st.markdown("**Top 5 At-Risk Municipalities:**")
    top_risk = risk_df.head(5)
    
    for idx, row in top_risk.iterrows():
        risk_color = {
            'Critical': '#DC2626',
            'High': '#EA580C', 
            'Moderate': '#D97706',
            'Low': '#059669'
        }.get(row['risk_level'], '#6B7280')
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 0.5rem; margin: 0.25rem 0; background: #F9FAFB; border-radius: 8px; border-left: 4px solid {risk_color};">
            <div style="flex: 1; font-weight: 600;">{row['municipality']}</div>
            <div style="text-align: right;">
                <span style="color: {risk_color}; font-weight: 700;">{row['total_cases']:.0f} cases</span>
                <span style="color: #6B7280; font-size: 0.85rem; margin-left: 1rem;">Risk: {row['risk_score']:.1f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Model Performance
    st.markdown(render_section_header("Model Performance"), unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <strong>Evaluation:</strong> Train/Test Split (80/20) — 
        Training: {len(train_data)} weeks, Testing: {len(test_data)} weeks
    </div>
    """, unsafe_allow_html=True)
    
    # Train models for evaluation
    nb_train_model, nb_train_results = fit_negative_binomial(train_data)
    zinb_train_model, zinb_train_results = fit_zinb(train_data)
    markov_train_model, markov_train_results = fit_markov_switching_nb(train_data)
    
    col1, col2, col3 = st.columns(3)
    
    nb_test_pred = None
    zinb_test_pred = None
    markov_test_pred = None
    
    with col1:
        st.markdown("**Negative Binomial (NB)**")
        if nb_train_results and len(test_data) > 0:
            nb_test_pred = predict_with_model(nb_train_results, test_data, 'nb')
            if nb_test_pred is not None:
                nb_metrics = calculate_metrics(test_data['cases'].values, nb_test_pred)
                st.markdown(f"""
                <div class="perf-grid">
                    <div class="perf-item"><div class="val">{nb_metrics['MSE']:.2f}</div><div class="lbl">MSE</div></div>
                    <div class="perf-item"><div class="val">{nb_metrics['RMSE']:.2f}</div><div class="lbl">RMSE</div></div>
                    <div class="perf-item"><div class="val">{nb_metrics['MAE']:.2f}</div><div class="lbl">MAE</div></div>
                    <div class="perf-item"><div class="val">{nb_metrics['MASE']:.2f}</div><div class="lbl">MASE</div></div>
                    <div class="perf-item"><div class="val">{nb_metrics['Accuracy']:.1f}%</div><div class="lbl">Accuracy</div></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Could not compute NB metrics")
    
    with col2:
        st.markdown("**Zero-Inflated NB (ZINB)**")
        if zinb_train_results and len(test_data) > 0:
            zinb_test_pred = predict_with_model(zinb_train_results, test_data, 'zinb')
            if zinb_test_pred is not None:
                zinb_metrics = calculate_metrics(test_data['cases'].values, zinb_test_pred)
                st.markdown(f"""
                <div class="perf-grid">
                    <div class="perf-item"><div class="val">{zinb_metrics['MSE']:.2f}</div><div class="lbl">MSE</div></div>
                    <div class="perf-item"><div class="val">{zinb_metrics['RMSE']:.2f}</div><div class="lbl">RMSE</div></div>
                    <div class="perf-item"><div class="val">{zinb_metrics['MAE']:.2f}</div><div class="lbl">MAE</div></div>
                    <div class="perf-item"><div class="val">{zinb_metrics['MASE']:.2f}</div><div class="lbl">MASE</div></div>
                    <div class="perf-item"><div class="val">{zinb_metrics['Accuracy']:.1f}%</div><div class="lbl">Accuracy</div></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Could not compute ZINB metrics")
    
    with col3:
        st.markdown("**Markov-Switching NB**")
        if markov_train_results and len(test_data) > 0:
            markov_test_pred = predict_with_model(markov_train_results, test_data, 'markov')
            if markov_test_pred is not None:
                markov_metrics = calculate_metrics(test_data['cases'].values, markov_test_pred)
                st.markdown(f"""
                <div class="perf-grid">
                    <div class="perf-item"><div class="val">{markov_metrics['MSE']:.2f}</div><div class="lbl">MSE</div></div>
                    <div class="perf-item"><div class="val">{markov_metrics['RMSE']:.2f}</div><div class="lbl">RMSE</div></div>
                    <div class="perf-item"><div class="val">{markov_metrics['MAE']:.2f}</div><div class="lbl">MAE</div></div>
                    <div class="perf-item"><div class="val">{markov_metrics['MASE']:.2f}</div><div class="lbl">MASE</div></div>
                    <div class="perf-item"><div class="val">{markov_metrics['Accuracy']:.1f}%</div><div class="lbl">Accuracy</div></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Could not compute Markov metrics")
    
    # Goodness of Fit Statistics (AIC/BIC)
    st.markdown(render_section_header("Goodness of Fit Statistics (Model Selection)"), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>AIC (Akaike Information Criterion)</strong> and <strong>BIC (Bayesian Information Criterion)</strong> 
        assess model fit while penalizing complexity. <strong>Lower values indicate better models.</strong>
        BIC penalizes model complexity more heavily than AIC.
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate AIC/BIC for all models
    aic_bic_data = []
    n_train = len(train_data)
    
    if nb_train_results:
        nb_aic_bic = calculate_aic_bic(nb_train_results, n_train, 'nb')
        aic_bic_data.append({
            'Model': 'Negative Binomial (NB)',
            'AIC': round(nb_aic_bic['AIC'], 2),
            'BIC': round(nb_aic_bic['BIC'], 2),
            'Parameters': len(nb_train_results.params)
        })
    
    if zinb_train_results:
        zinb_aic_bic = calculate_aic_bic(zinb_train_results, n_train, 'zinb')
        aic_bic_data.append({
            'Model': 'Zero-Inflated NB (ZINB)',
            'AIC': round(zinb_aic_bic['AIC'], 2),
            'BIC': round(zinb_aic_bic['BIC'], 2),
            'Parameters': len(zinb_train_results.params)
        })
    
    if markov_train_results:
        markov_aic_bic = calculate_aic_bic(markov_train_results, n_train, 'markov')
        aic_bic_data.append({
            'Model': 'Markov-Switching NB',
            'AIC': round(markov_aic_bic['AIC'], 2),
            'BIC': round(markov_aic_bic['BIC'], 2),
            'Parameters': len(markov_train_results.params)
        })
    
    if aic_bic_data:
        aic_bic_df = pd.DataFrame(aic_bic_data)
        
        # Identify best models
        if not aic_bic_df['AIC'].isna().all():
            best_aic_idx = aic_bic_df['AIC'].idxmin()
            aic_bic_df['Best AIC'] = ''
            aic_bic_df.loc[best_aic_idx, 'Best AIC'] = '✓ Best'
        
        if not aic_bic_df['BIC'].isna().all():
            best_bic_idx = aic_bic_df['BIC'].idxmin()
            aic_bic_df['Best BIC'] = ''
            aic_bic_df.loc[best_bic_idx, 'Best BIC'] = '✓ Best'
        
        # Style the dataframe
        def highlight_best(row):
            if '✓ Best' in str(row.get('Best AIC', '')) or '✓ Best' in str(row.get('Best BIC', '')):
                return ['background-color: #D1FAE5'] * len(row)
            else:
                return ['background-color: #F9FAFB'] * len(row)
        
        styled_aic_bic = aic_bic_df.style.apply(highlight_best, axis=1)
        st.dataframe(styled_aic_bic, use_container_width=True, hide_index=True)
        
        # Interpretation
        st.markdown("**Model Selection Recommendation:**")
        
        if not aic_bic_df['AIC'].isna().all() and not aic_bic_df['BIC'].isna().all():
            best_aic_model = aic_bic_df.loc[best_aic_idx, 'Model']
            best_bic_model = aic_bic_df.loc[best_bic_idx, 'Model']
            
            if best_aic_model == best_bic_model:
                st.markdown(f"""
                <div style="padding: 1rem; background: #D1FAE5; border-radius: 8px; border-left: 4px solid #10B981;">
                    <strong>✓ Recommended Model: {best_aic_model}</strong><br>
                    Both AIC and BIC criteria agree that this model provides the best balance between 
                    goodness of fit and model complexity.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="padding: 1rem; background: #FEF3C7; border-radius: 8px; border-left: 4px solid #F59E0B;">
                    <strong>⚠ Mixed Results:</strong><br>
                    • AIC prefers: <strong>{best_aic_model}</strong> (more complex model may be justified)<br>
                    • BIC prefers: <strong>{best_bic_model}</strong> (simpler model preferred)<br>
                    Consider both criteria along with domain knowledge for final model selection.
                </div>
                """, unsafe_allow_html=True)
        
        # Visual comparison
        col1, col2 = st.columns(2)
        
        with col1:
            fig_aic = px.bar(
                aic_bic_df,
                x='Model',
                y='AIC',
                title='AIC Comparison (Lower is Better)',
                color='AIC',
                color_continuous_scale='RdYlGn_r',
                text='AIC'
            )
            fig_aic.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_aic.update_layout(
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=False,
                xaxis_title='',
                yaxis_title='AIC Value'
            )
            st.plotly_chart(fig_aic, use_container_width=True)
        
        with col2:
            fig_bic = px.bar(
                aic_bic_df,
                x='Model',
                y='BIC',
                title='BIC Comparison (Lower is Better)',
                color='BIC',
                color_continuous_scale='RdYlGn_r',
                text='BIC'
            )
            fig_bic.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_bic.update_layout(
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=False,
                xaxis_title='',
                yaxis_title='BIC Value'
            )
            st.plotly_chart(fig_bic, use_container_width=True)
    else:
        st.warning("No models available for AIC/BIC comparison")
    
    # Actual vs Predicted Chart
    if nb_test_pred is not None or zinb_test_pred is not None or markov_test_pred is not None:
        st.markdown("**Actual vs Predicted (Test Set)**")
        
        fig_compare = go.Figure()
        fig_compare.add_trace(go.Scatter(
            y=test_data['cases'].values,
            mode='lines+markers',
            name='Actual',
            line=dict(color='#1F2937', width=2)
        ))
        
        if nb_test_pred is not None:
            fig_compare.add_trace(go.Scatter(
                y=nb_test_pred,
                mode='lines+markers',
                name='NB Predicted',
                line=dict(color='#667eea', width=2, dash='dash')
            ))
        
        if zinb_test_pred is not None:
            fig_compare.add_trace(go.Scatter(
                y=zinb_test_pred,
                mode='lines+markers',
                name='ZINB Predicted',
                line=dict(color='#10B981', width=2, dash='dot')
            ))
        
        if markov_test_pred is not None:
            fig_compare.add_trace(go.Scatter(
                y=markov_test_pred,
                mode='lines+markers',
                name='Markov Predicted',
                line=dict(color='#F59E0B', width=2, dash='dashdot')
            ))
        
        fig_compare.update_layout(
            height=300,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis_title="Test Period",
            yaxis_title="Cases",
            margin=dict(t=40)
        )
        st.plotly_chart(fig_compare, use_container_width=True)
    
    # Significant Factors Section
    st.markdown(render_section_header("Significant Factors Analysis"), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        Analysis of factors that significantly influence dengue case counts. 
        Factors with <strong>p-value < 0.05</strong> are considered statistically significant.
    </div>
    """, unsafe_allow_html=True)
    
    # Fit model with environmental variables
    nb_env_results, feature_names = fit_nb_with_env(full_time_series)
    
    if nb_env_results is not None and feature_names is not None:
        # Extract coefficients and p-values
        try:
            coefs = nb_env_results.params
            pvalues = nb_env_results.pvalues
            conf_int = nb_env_results.conf_int()
            
            # Create significance table
            sig_data = []
            for i, name in enumerate(feature_names):
                # Safely extract values
                if i >= len(coefs):
                    continue
                    
                coef = coefs[i]
                pval = pvalues[i] if i < len(pvalues) else 1.0
                
                # Handle confidence intervals - could be DataFrame or array
                try:
                    if hasattr(conf_int, 'iloc'):
                        # DataFrame format
                        ci_low = conf_int.iloc[i, 0]
                        ci_high = conf_int.iloc[i, 1]
                    else:
                        # Array format
                        ci_low = conf_int[i, 0]
                        ci_high = conf_int[i, 1]
                except (IndexError, KeyError):
                    ci_low = coef - 1.96 * nb_env_results.bse[i] if i < len(nb_env_results.bse) else coef
                    ci_high = coef + 1.96 * nb_env_results.bse[i] if i < len(nb_env_results.bse) else coef
                
                # Determine significance
                if pval < 0.001:
                    sig_level = '***'
                    sig_text = 'Highly Significant'
                elif pval < 0.01:
                    sig_level = '**'
                    sig_text = 'Very Significant'
                elif pval < 0.05:
                    sig_level = '*'
                    sig_text = 'Significant'
                else:
                    sig_level = ''
                    sig_text = 'Not Significant'
                
                # Effect direction
                if name != 'Intercept':
                    if coef > 0:
                        effect = '↑ Increases cases'
                    else:
                        effect = '↓ Decreases cases'
                else:
                    effect = '-'
                
                sig_data.append({
                    'Factor': name,
                    'Coefficient': round(float(coef), 4),
                    'p-value': f"{float(pval):.4f}",
                    'Significance': f"{sig_text} {sig_level}",
                    'Effect': effect,
                    '95% CI': f"[{float(ci_low):.3f}, {float(ci_high):.3f}]"
                })
            
            sig_df = pd.DataFrame(sig_data)
            
            # Display table
            def highlight_significance(row):
                if '***' in row['Significance'] or '**' in row['Significance']:
                    return ['background-color: #D1FAE5'] * len(row)
                elif '*' in row['Significance']:
                    return ['background-color: #FEF3C7'] * len(row)
                else:
                    return ['background-color: #F9FAFB'] * len(row)
            
            styled_sig = sig_df.style.apply(highlight_significance, axis=1)
            st.dataframe(styled_sig, use_container_width=True, hide_index=True)
            
            # Visual representation
            st.markdown("**Factor Importance (Absolute Coefficient)**")
            
            factor_importance = sig_df[sig_df['Factor'] != 'Intercept'].copy()
            factor_importance['Abs_Coef'] = factor_importance['Coefficient'].abs()
            factor_importance = factor_importance.sort_values('Abs_Coef', ascending=True)
            
            fig_importance = px.bar(
                factor_importance,
                x='Abs_Coef',
                y='Factor',
                orientation='h',
                color='Coefficient',
                color_continuous_scale='RdYlGn_r',
                labels={'Abs_Coef': 'Absolute Coefficient', 'Factor': ''}
            )
            fig_importance.update_layout(
                height=250,
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=False,
                coloraxis_showscale=True,
                coloraxis_colorbar=dict(title='Effect')
            )
            st.plotly_chart(fig_importance, use_container_width=True)
            
            # Key findings
            st.markdown("**Key Findings:**")
            
            significant_factors = [row for _, row in sig_df.iterrows() 
                                  if '*' in row['Significance'] and row['Factor'] != 'Intercept']
            
            if significant_factors:
                for factor in significant_factors:
                    direction = "increases" if factor['Coefficient'] > 0 else "decreases"
                    st.markdown(f"""
                    <div style="padding: 0.5rem; margin: 0.25rem 0; background: #F0FDF4; border-radius: 8px; border-left: 4px solid #10B981;">
                        <strong>{factor['Factor']}</strong> significantly {direction} dengue cases 
                        <span style="color: #6B7280;">(p = {factor['p-value']}, coefficient = {factor['Coefficient']:.4f})</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No factors reached statistical significance at p < 0.05 level.")
                
        except Exception as e:
            st.warning(f"Could not extract model coefficients: {e}")
    else:
        st.warning("Could not fit model with environmental variables for significance analysis.")
    
    # Methodology
    with st.expander("Methodology"):
        st.markdown("""
        ### Negative Binomial Regression
        
        Appropriate for overdispersed count data where variance exceeds the mean.
        
        $$P(Y = y) = \\binom{y + r - 1}{y} p^r (1-p)^y$$
        
        ### Zero-Inflated Negative Binomial (ZINB)
        
        Extends NB to handle excess zeros:
        
        $$P(Y = 0) = \\pi + (1-\\pi) \\cdot NB(0)$$
        $$P(Y = y) = (1-\\pi) \\cdot NB(y), \\quad y > 0$$
        
        ### Markov-Switching Negative Binomial (MS-NB)
        
        Captures regime changes (e.g., outbreak vs. endemic states) using hidden Markov model:
        
        - **2 regimes**: Low transmission (endemic) and high transmission (epidemic)
        - **Switching dynamics**: Probabilistic transitions between states
        - **Regime-dependent parameters**: Different distributions in each state
        
        Transition probability matrix:
        $$P(S_t = j | S_{t-1} = i), \\quad i,j \\in \\{1,2\\}$$
        
        ### Goodness of Fit Criteria
        
        #### Akaike Information Criterion (AIC)
        
        $$AIC = 2k - 2\\ln(L)$$
        
        where:
        - $k$ = number of parameters in the model
        - $L$ = maximum likelihood of the model
        
        **Interpretation**: Lower AIC values indicate better model fit. AIC balances model fit with complexity 
        but is more lenient toward complex models.
        
        #### Bayesian Information Criterion (BIC)
        
        $$BIC = k \\ln(n) - 2\\ln(L)$$
        
        where:
        - $k$ = number of parameters
        - $n$ = number of observations
        - $L$ = maximum likelihood
        
        **Interpretation**: Lower BIC values indicate better model fit. BIC penalizes model complexity more 
        heavily than AIC, preferring simpler models.
        
        #### Model Selection Guidelines
        
        - **AIC**: Useful when prediction accuracy is the primary goal
        - **BIC**: Preferred when identifying the "true" model and avoiding overfitting
        - **ΔIC > 10**: Substantial evidence for the better model
        - **ΔIC = 4-7**: Considerably less support for the model with higher IC
        - **ΔIC < 2**: Models are essentially equivalent
        
        ### Statistical Significance
        
        - **p < 0.001 (***)**:  Highly significant
        - **p < 0.01 (**)**: Very significant
        - **p < 0.05 (*)**: Significant
        - **p ≥ 0.05**: Not significant
        
        ### Risk Calculation
        
        Risk scores are calculated based on:
        - Total cases in the analysis window
        - Normalized to 0-100 scale
        - Categories: Low (0-25), Moderate (25-50), High (50-75), Critical (75-100)
        """)
    
    
    # Footer
    st.markdown(render_footer(), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
