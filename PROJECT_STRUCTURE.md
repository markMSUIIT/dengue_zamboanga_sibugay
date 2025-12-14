# Project Structure & File Guide

## 📁 Project Directory Layout

```
brent_final_thesis_py/
│
├── 📄 app.py                           # Main Streamlit application
├── 📄 analysis_module.py               # Advanced statistical analysis tools
├── 📄 verify_setup.py                  # Installation verification script
│
├── 📋 requirements.txt                 # Python dependencies
├── 🚀 run.sh                           # Quick launch script
│
├── 📚 README.md                        # Full project documentation
├── 📘 QUICK_START.md                   # 5-minute setup guide
├── 📗 THESIS_GUIDE.md                  # Academic research guidelines
├── 📄 PROJECT_STRUCTURE.md             # This file
│
├── 📊 sibugay_dengue_cases_dataset.csv # Your data file (should be here)
│
└── .streamlit/
    └── config.toml                     # Streamlit configuration
```

---

## 📄 File Descriptions

### Core Application Files

#### `app.py` (Main Dashboard)
**Purpose:** Complete Streamlit application for dengue analysis
**Size:** ~600 lines
**Features:**
- 5 interactive analysis tabs
- Real-time filtering and updates
- 50+ interactive visualizations
- Professional theme and styling
- Responsive layout

**Key Sections:**
1. Data loading and preprocessing
2. Page configuration
3. Sidebar filters
4. Key metrics display
5. Tab 1: Temporal trends
6. Tab 2: Geographic analysis
7. Tab 3: Environmental factors
8. Tab 4: Statistical analysis
9. Tab 5: Correlation matrix

**Dependencies Required:**
- streamlit
- pandas
- plotly
- numpy

---

#### `analysis_module.py` (Analysis Tools)
**Purpose:** Advanced statistical analysis functions
**Size:** ~200 lines
**Classes:**
- `DengueAnalyzer`: Main analysis class with methods:
  - `trend_analysis()`: Temporal trend calculation
  - `seasonality_detection()`: Seasonal pattern identification
  - `environmental_impact()`: Climate correlation analysis
  - `spatial_analysis()`: Geographic variation assessment
  - `risk_stratification()`: Municipal risk ranking
  - `outbreak_detection()`: Anomaly identification
  - `calculate_statistics()`: Summary statistics

- `ThesisReportGenerator`: Report generation utilities
- `quality_assessment()`: Data quality validation

**Usage in Thesis:**
```python
from analysis_module import DengueAnalyzer
analyzer = DengueAnalyzer(df)
```

---

#### `verify_setup.py` (Verification Tool)
**Purpose:** Validates installation and data setup
**Size:** ~150 lines
**Checks:**
- Python version (3.8+)
- All dependencies installed
- Data file exists and readable
- Required columns present
- Configuration files present

**Run:** `python3 verify_setup.py`

**Output:**
- ✅/❌ status for each check
- Instructions if issues found

---

### Configuration Files

#### `requirements.txt`
**Purpose:** Python package dependencies
**Contents:**
```
streamlit==1.28.1
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
scipy==1.11.2
scikit-learn==1.3.0
```

**Installation:** `pip install -r requirements.txt`

---

#### `.streamlit/config.toml`
**Purpose:** Streamlit application configuration
**Customizes:**
- Color theme (primary red, light background)
- Page layout
- Logging level
- Server settings

**Edit to:** Change colors, modify server settings

---

#### `run.sh`
**Purpose:** Automated launch script for macOS/Linux
**Does:**
1. Checks Python installation
2. Verifies requirements.txt exists
3. Installs/updates dependencies
4. Launches Streamlit app
5. Opens browser at localhost:8501

**Usage:** `bash run.sh` or `./run.sh`

---

### Documentation Files

#### `README.md` (Comprehensive Guide)
**Purpose:** Complete project documentation
**Sections:**
- Features overview
- Installation instructions
- Usage guidelines
- Data requirements
- Dashboard sections
- Variable explanations
- Technical stack
- Future enhancements

**Audience:** All users
**Read First:** If new to project

---

#### `QUICK_START.md` (Fast Setup)
**Purpose:** Get running in 5 minutes
**Sections:**
- Quick setup (2 steps)
- Navigation guide
- Tab-by-tab explanation
- Filter guide
- Visualization interpretation
- Tips for research
- Troubleshooting
- Column reference table

**Audience:** Users ready to run
**Best For:** Immediate usage

---

#### `THESIS_GUIDE.md` (Academic Focus)
**Purpose:** Guidance for thesis research
**Sections:**
- Research focus areas (4 main topics)
- Thesis chapter structure
- Key graphs to include
- Statistics to report
- Analysis workflow (7 steps)
- Quality checklist
- Sample methods text
- Publication recommendations
- Critical analysis questions

**Audience:** Thesis/research students
**Best For:** Academic preparation

---

#### `PROJECT_STRUCTURE.md` (This File)
**Purpose:** Overview of all project files
**Contents:**
- Directory structure
- File descriptions
- Quick reference
- Setup instructions
- Usage examples

---

### Data File

#### `sibugay_dengue_cases_dataset.csv`
**Purpose:** Your dengue surveillance data
**Format:** CSV (comma-separated values)
**Location:** Should be in project root directory

**Required Columns:**
| Column | Type | Description |
|--------|------|-------------|
| MUNICIPALITY | Text | Location name |
| YEAR_2 | Integer | Calendar year |
| MONTH | Integer | Month (1-12) |
| WEEK | Integer | Week (1-52) |
| QUARTER | Integer | Quarter (1-4) |
| CASES | Integer | Confirmed cases |
| MORBIDITY_WEEK | Float | Weekly rate |
| T2M_MAX | Float | Max temp (°C) |
| T2M_MIN | Float | Min temp (°C) |
| RH2M | Float | Humidity (%) |
| PRECTOTCORR | Float | Precipitation (mm) |

---

## 🚀 Getting Started

### 1️⃣ Initial Setup
```bash
# Navigate to project directory
cd /Users/most-project/Downloads/brent_final_thesis_py

# Verify setup
python3 verify_setup.py

# Install dependencies (if needed)
pip install -r requirements.txt
```

### 2️⃣ Launch Application
```bash
# Option A: Direct launch
streamlit run app.py

# Option B: Using script
bash run.sh
```

### 3️⃣ Access Dashboard
- Browser opens automatically
- Or navigate to: http://localhost:8501

---

## 📊 Quick Reference

### For Different Users

**New User?**
→ Read: QUICK_START.md
→ Run: `streamlit run app.py`

**Thesis Student?**
→ Read: THESIS_GUIDE.md
→ Use: Analysis tabs in specific order
→ Export: Charts for thesis

**Advanced User?**
→ Edit: app.py for customizations
→ Use: analysis_module.py for deeper analysis
→ Extend: Add new functions

**Data Scientist?**
→ Import: analysis_module.py
→ Extend: Create new analyzer methods
→ Export: Data for ML models

---

## 🔧 Customization Guide

### Modify Colors
**File:** `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#FF6B6B"      # Change primary color
backgroundColor = "#FFFFFF"   # Change background
```

### Add New Visualizations
**File:** `app.py`
1. Import plotly visualization
2. Create data aggregation
3. Add figure to appropriate tab
4. Update layout and styling

### Create New Analysis Functions
**File:** `analysis_module.py`
1. Add method to `DengueAnalyzer` class
2. Include documentation
3. Return pandas DataFrame or dict
4. Add usage example

### Example - Custom Analysis
```python
def custom_analysis(self):
    """Your custom analysis"""
    result = self.df.groupby('MUNICIPALITY')['CASES'].mean()
    return result
```

---

## ✅ File Checklist

Before running, ensure you have:
- [ ] `app.py` - Main application
- [ ] `analysis_module.py` - Analysis tools
- [ ] `requirements.txt` - Dependencies list
- [ ] `.streamlit/config.toml` - Configuration
- [ ] `sibugay_dengue_cases_dataset.csv` - Data file
- [ ] `README.md` - Documentation
- [ ] `QUICK_START.md` - Setup guide
- [ ] `THESIS_GUIDE.md` - Academic guide

**Optional but recommended:**
- [ ] `run.sh` - Launch script
- [ ] `verify_setup.py` - Verification tool
- [ ] `PROJECT_STRUCTURE.md` - This file

---

## 🐛 Troubleshooting

### Missing Files
**Problem:** File not found error
**Solution:** Ensure all files are in project directory

### Import Errors
**Problem:** Module not found
**Solution:** Run `pip install -r requirements.txt`

### Data Not Loading
**Problem:** CSV file error
**Solution:** 
1. Check file name (case-sensitive)
2. Verify file location
3. Run `python3 verify_setup.py`

### App Won't Start
**Problem:** Streamlit error
**Solution:**
```bash
pip install --upgrade streamlit
streamlit run app.py --logger.level=debug
```

---

## 📞 Support

### Quick Help
1. Run `python3 verify_setup.py` - Checks everything
2. Read `QUICK_START.md` - Common questions
3. Check `THESIS_GUIDE.md` - Academic help
4. Review `README.md` - Full documentation

### Common Issues
- **Slow dashboard:** Filter year range
- **Missing data:** Check CSV columns
- **No visualizations:** Verify data loads correctly
- **Theme issues:** Edit config.toml

---

## 📈 Project Statistics

| Metric | Value |
|--------|-------|
| Total Files | 13 |
| Code Lines | 1,000+ |
| Visualizations | 50+ |
| Analysis Tabs | 5 |
| Documentation Pages | 4 |
| Supported Municipalities | Multiple |
| Data Variables | 11+ |
| Interactive Features | 100+ |

---

## 🎓 Academic Credentials

**Project Type:** Thesis Research Dashboard
**Application:** Epidemiological Analysis
**Subject Area:** Infectious Disease Surveillance
**Focus Region:** Zamboanga Sibugay, Philippines
**Data Type:** Surveillance + Environmental
**Visualization:** Interactive & Publication-Quality

---

## 📅 Version Information

**Current Version:** 1.0
**Release Date:** December 2025
**Python:** 3.8-3.11
**Streamlit:** 1.28.1+
**Last Updated:** December 2025

---

## 📋 Changelog

### Version 1.0 (Initial Release)
- ✅ Complete Streamlit dashboard
- ✅ 5 analysis tabs
- ✅ 50+ visualizations
- ✅ Statistical analysis tools
- ✅ Comprehensive documentation
- ✅ Thesis-specific guidance
- ✅ Environmental analysis
- ✅ Interactive filtering

---

**Happy analyzing! 🦟📊**

For detailed information, see respective documentation files.
