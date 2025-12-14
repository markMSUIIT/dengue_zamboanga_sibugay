# Quick Start Guide - Dengue Analysis Dashboard

## ⚡ Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
streamlit run app.py
```

Or use the provided script:
```bash
bash run.sh
```

The app will open at `http://localhost:8501`

---

## 📚 Dashboard Usage Guide

### Navigation
1. **Sidebar** - Left panel for filtering data
   - Select municipalities (single or multiple)
   - Choose year range
   - View updates in real-time

2. **Metric Cards** - Top section showing key statistics
   - Total cases
   - Average morbidity rate
   - Temperature and humidity

3. **Tabs** - Main analysis sections
   - 📈 Temporal Trends
   - 🗺️ Geographic Analysis
   - 🌡️ Environmental Factors
   - 📊 Statistical Analysis
   - 🔬 Correlation Matrix

---

## 📊 Analysis Tabs Explained

### Tab 1: Temporal Trends
Shows how dengue cases change over time:
- **Weekly line chart**: Cases week-by-week progression
- **Monthly bar chart**: Total cases by month
- **Quarterly area chart**: Quarterly distribution patterns

**Use for:** Identifying peak seasons and temporal patterns

### Tab 2: Geographic Analysis
Municipality-level insights:
- **Horizontal bar chart**: Total cases by municipality
- **Morbidity rates**: Risk comparison across areas
- **Year comparison**: Multi-year trends by location

**Use for:** Identifying high-risk municipalities

### Tab 3: Environmental Factors
Relationship between climate and dengue:
- **Temperature trends**: Max temperature vs cases
- **Humidity patterns**: Relative humidity effects
- **Precipitation impact**: Rainfall and outbreak correlation
- **Temperature range**: Daily variation effects

**Use for:** Understanding environmental drivers

### Tab 4: Statistical Analysis
Quantitative summaries:
- **Descriptive statistics**: Mean, median, std deviation
- **Distributions**: Case frequency histograms
- **Box plots**: Outlier detection by location

**Use for:** Statistical reporting and validation

### Tab 5: Correlation Analysis
Variable relationships:
- **Heatmap**: All correlations at glance
- **Bar chart**: Strongest relationships identified

**Use for:** Identifying important predictive factors

---

## 🔍 Filter Guide

### Municipality Selection
- **Single selection**: Focus on one area
- **Multiple selection**: Compare municipalities
- Click "Clear all" to reset
- Default: All municipalities

### Year Range Slider
- Adjust for specific time periods
- Includes all years in dataset
- Updates all visualizations instantly

---

## 📈 Interpreting Visualizations

### Line Charts
- 🔴 Upward trend = Increasing cases
- 🔵 Downward trend = Decreasing cases
- Peaks = Outbreak periods

### Bar Charts
- Taller bars = Higher values
- Color intensity = Magnitude
- Sorted for easy comparison

### Heat Maps
- 🔴 Red = Strong positive correlation
- 🔵 Blue = Strong negative correlation
- White = No correlation

### Box Plots
- Box = Middle 50% of data
- Line in box = Median
- Dots outside = Outliers

---

## 💡 Tips for Thesis Research

### Data Selection
1. Filter to specific municipalities
2. Focus on relevant year range
3. Note seasonal patterns
4. Check for data quality issues

### Analysis Approach
1. Start with temporal trends
2. Move to geographic patterns
3. Investigate environmental factors
4. Validate with statistical tests
5. Document correlations

### Documentation
- Take screenshots of key findings
- Export data for tables
- Note outliers and anomalies
- Document filtering choices

### Export Data
Right-click on any chart and select "Download as PNG"
For tables: Copy data using the icon in top-right

---

## 🔧 Troubleshooting

### Issue: App won't start
**Solution:** 
```bash
pip install --upgrade -r requirements.txt
streamlit run app.py
```

### Issue: Data not loading
**Check:**
- CSV file in correct directory
- Column names match specification
- No special characters in paths

### Issue: Slow performance
**Solution:**
- Reduce time range filter
- Select fewer municipalities
- Close other browser tabs

### Issue: Missing columns
**Error indicates:** Column not in dataset
**Fix:** Verify CSV has all required columns

---

## 📋 Data Columns Reference

| Column | Type | Range | Meaning |
|--------|------|-------|---------|
| MUNICIPALITY | Text | - | Location name |
| YEAR_2 | Integer | 2020-2024 | Calendar year |
| MONTH | Integer | 1-12 | Month number |
| WEEK | Integer | 1-52 | Week of year |
| QUARTER | Integer | 1-4 | Quarter |
| CASES | Integer | 0-100+ | Confirmed cases |
| MORBIDITY_WEEK | Float | 0-1.0 | Weekly rate |
| T2M_MAX | Float | 20-35°C | Max temperature |
| T2M_MIN | Float | 15-30°C | Min temperature |
| RH2M | Float | 50-100% | Relative humidity |
| PRECTOTCORR | Float | 0-300mm | Precipitation |

---

## 📞 Getting Help

### Common Questions

**Q: What does morbidity rate mean?**
A: Cases per 1,000 population per week

**Q: Why are some weeks missing?**
A: Incomplete reporting or zero cases

**Q: Can I modify the dashboard?**
A: Yes! Edit `app.py` to customize visualizations

**Q: How do I export data?**
A: Use browser's download feature on charts or copy tables

---

## 🎓 Academic Use

### For Thesis/Research Papers
- Screenshot all analysis tabs
- Document filtering criteria
- Report key statistics
- Cite environmental factors
- Note temporal trends
- Include correlation findings

### For Presentations
- Use interactive dashboard for live demos
- Export charts as high-resolution images
- Create custom filtered views
- Highlight key metrics

### For Reports
- Generate summary statistics (Tab 4)
- Show geographic distribution (Tab 2)
- Display temporal patterns (Tab 1)
- Include correlation findings (Tab 5)

---

## 🚀 Advanced Features

### Using Analysis Module
```python
from analysis_module import DengueAnalyzer

analyzer = DengueAnalyzer(df)
trends = analyzer.trend_analysis('CASES')
outbreak_weeks = analyzer.outbreak_detection()
risk_levels = analyzer.risk_stratification()
```

### Customization
Edit `app.py` to:
- Add new visualizations
- Change colors/themes
- Modify calculations
- Add new analysis sections

---

## 📅 Update Log

- **v1.0** (Dec 2025) - Initial release with 5 analysis tabs
- Full interactive Streamlit dashboard
- 50+ customizable visualizations
- Environmental factor analysis
- Statistical summary tools

---

**Last Updated:** December 2025
**Dashboard Version:** 1.0
**Recommended Python:** 3.8-3.11

Happy analyzing! 🦟📊
