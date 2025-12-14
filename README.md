# Dengue Cases Analysis Dashboard - Zamboanga Sibugay

A comprehensive thesis-worthy Streamlit dashboard for analyzing dengue epidemiology in Zamboanga Sibugay, Philippines. This application integrates temporal, spatial, and environmental factors to provide insights into dengue transmission patterns.

## Features

### 📊 Core Analysis Modules

1. **Temporal Trends**
   - Weekly case progression
   - Monthly pattern analysis
   - Quarterly distribution
   - Year-over-year comparisons

2. **Geographic Analysis**
   - Municipality-level case distribution
   - Morbidity rate by location
   - Comparative analysis across regions
   - Spatial risk assessment

3. **Environmental Factors**
   - Temperature-case relationship
   - Humidity correlation analysis
   - Precipitation impact assessment
   - Temperature range effects

4. **Statistical Analysis**
   - Descriptive statistics
   - Distribution analysis
   - Box plots and outlier detection
   - Summary tables

5. **Correlation Analysis**
   - Pearson correlation matrix
   - Environmental-epidemiological relationships
   - Variable dependency analysis

## Installation

### Requirements
- Python 3.8+
- pip or conda

### Setup

1. Clone or download this repository
2. Navigate to the project directory:
```bash
cd /Users/most-project/Downloads/brent_final_thesis_py
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure your data file is present:
```
sibugay_dengue_cases_dataset.csv
```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Data Requirements

The dataset should include the following columns:
- `MUNICIPALITY`: Municipal identifier
- `YEAR_2`: Year of observation
- `MONTH`: Month (1-12)
- `WEEK`: Week of year (1-52)
- `QUARTER`: Quarter (1-4)
- `CASES`: Number of confirmed dengue cases
- `MORBIDITY_WEEK`: Weekly morbidity rate
- `T2M_MAX`: Maximum temperature (°C)
- `T2M_MIN`: Minimum temperature (°C)
- `RH2M`: Relative humidity at 2m (%)
- `PRECTOTCORR`: Corrected precipitation (mm)

## Dashboard Sections

### 🔍 Navigation
- Use the sidebar to filter by municipality and year range
- View real-time metrics and trends
- Switch between analysis tabs for different perspectives

### 📈 Key Metrics
- Total confirmed cases
- Average weekly morbidity
- Temperature statistics
- Humidity levels

### 🔧 Filtering Options
- **Municipality Selection**: Filter data by one or multiple municipalities
- **Year Range**: Select specific years for analysis
- **Dynamic Updates**: All visualizations update in real-time

## Visualizations

All visualizations are interactive:
- Hover for detailed information
- Click legend items to toggle series
- Use tools to zoom, pan, and download
- Compare multiple variables simultaneously

## Variables Explained

### Epidemiological
- **Cases**: Weekly confirmed dengue cases
- **Morbidity Rate**: Ratio of new cases to population at risk

### Environmental
- **Temperature**: Max/Min daily temperatures influence mosquito breeding
- **Humidity**: High humidity favors dengue vector survival
- **Precipitation**: Rainfall creates breeding sites for Aedes mosquitoes

## Thesis Applications

This dashboard is suitable for:
- ✅ Descriptive epidemiology analysis
- ✅ Temporal trend identification
- ✅ Environmental risk factor assessment
- ✅ Geospatial disease distribution
- ✅ Predictive modeling foundation
- ✅ Public health surveillance reporting

## Data Interpretation Guide

### Correlation Strength
- **0.7-1.0**: Strong correlation
- **0.4-0.7**: Moderate correlation
- **0.2-0.4**: Weak correlation
- **0.0-0.2**: Very weak/no correlation

### High-Risk Indicators
- Peak cases in specific months/quarters
- Municipalities with sustained high case counts
- Temperature and humidity in optimal ranges for vector
- Correlation with environmental factors

## Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (interactive charts)
- **Analysis**: SciPy, Scikit-learn ready
- **Language**: Python 3.8+

## Future Enhancements

- Time series forecasting models
- Interactive heat maps with geographic data
- Real-time data integration
- Predictive risk zones
- Export functionality (PDF reports)
- Machine learning model integration

## Citation

If using this analysis in academic work, please reference:
```
Dengue Epidemiological Analysis - Zamboanga Sibugay
Integrated Health Surveillance System Data
[Year]
```

## License

This project is provided for educational and research purposes.

## Support

For issues or questions, ensure:
1. All dependencies are properly installed
2. Dataset columns match specification
3. Data is properly formatted (numeric values)
4. File paths are correct

## Author

Prepared for thesis research on dengue epidemiology in Zamboanga Sibugay

---

**Last Updated**: December 2025
**Dashboard Version**: 1.0
