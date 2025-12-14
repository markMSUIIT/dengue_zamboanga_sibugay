#!/usr/bin/env python3
"""
Installation and Data Verification Script
Checks if all dependencies are installed and data is ready
"""

import sys
import importlib
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Requires 3.8+")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    dependencies = {
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'plotly': 'Plotly',
        'scipy': 'SciPy',
    }
    
    all_installed = True
    
    for package, name in dependencies.items():
        try:
            importlib.import_module(package)
            print(f"✅ {name} - Installed")
        except ImportError:
            print(f"❌ {name} - NOT installed")
            all_installed = False
    
    return all_installed

def check_data_file():
    """Check if dataset exists and is readable"""
    data_file = Path('sibugay_dengue_cases_dataset.csv')
    
    if data_file.exists():
        try:
            import pandas as pd
            df = pd.read_csv(data_file)
            print(f"✅ Data File Found - {len(df)} rows, {len(df.columns)} columns")
            
            # Check key columns
            required_cols = ['MUNICIPALITY', 'YEAR_2', 'MONTH', 'WEEK', 'CASES', 
                           'T2M_MAX', 'T2M_MIN', 'RH2M', 'PRECTOTCORR']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                print(f"⚠️  Missing columns: {missing_cols}")
                return False
            else:
                print(f"✅ All required columns present")
                return True
        except Exception as e:
            print(f"❌ Error reading data file: {e}")
            return False
    else:
        print(f"❌ Data File NOT Found: sibugay_dengue_cases_dataset.csv")
        return False

def check_config_file():
    """Check if Streamlit config exists"""
    config_file = Path('.streamlit/config.toml')
    
    if config_file.exists():
        print("✅ Streamlit config file found")
        return True
    else:
        print("⚠️  Streamlit config file not found (will use defaults)")
        return True  # Not critical

def check_app_file():
    """Check if main app file exists"""
    app_file = Path('app.py')
    
    if app_file.exists():
        print("✅ Main app file (app.py) found")
        return True
    else:
        print("❌ Main app file (app.py) NOT found")
        return False

def main():
    """Run all checks"""
    print("\n" + "="*50)
    print("🦟 DENGUE DASHBOARD - VERIFICATION CHECK")
    print("="*50 + "\n")
    
    checks = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Data File": check_data_file(),
        "Config File": check_config_file(),
        "App File": check_app_file(),
    }
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    all_pass = all(checks.values())
    
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    print("="*50 + "\n")
    
    if all_pass:
        print("✅ All checks passed! You're ready to run:")
        print("   streamlit run app.py\n")
        return 0
    else:
        print("❌ Some checks failed. Please:")
        print("   1. Install missing dependencies: pip install -r requirements.txt")
        print("   2. Ensure sibugay_dengue_cases_dataset.csv is in the current directory")
        print("   3. Check that all required columns are present\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
