"""
Advanced Statistical Analysis Module for Dengue Epidemiology
Supports thesis research with comprehensive statistical tools
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

class DengueAnalyzer:
    """Comprehensive dengue epidemiological analysis"""
    
    def __init__(self, df):
        self.df = df.dropna(subset=['CASES'])
    
    def trend_analysis(self, column, period='MONTH'):
        """Analyze temporal trends"""
        trend_data = self.df.groupby(period)[column].agg(['mean', 'std', 'count', 'min', 'max'])
        return trend_data
    
    def seasonality_detection(self, window=4):
        """Detect seasonal patterns using moving average"""
        weekly_cases = self.df.groupby(['YEAR_2', 'WEEK'])['CASES'].sum().reset_index()
        weekly_cases['MA'] = weekly_cases['CASES'].rolling(window=window, center=True).mean()
        return weekly_cases
    
    def environmental_impact(self):
        """Analyze environmental factor impact on dengue"""
        results = {}
        
        # Temperature correlation
        temp_cols = ['T2M_MAX', 'T2M_MIN']
        for col in temp_cols:
            if col in self.df.columns:
                corr, p_val = pearsonr(self.df[col].dropna(), 
                                      self.df.loc[self.df[col].notna(), 'CASES'])
                results[col] = {'correlation': corr, 'p_value': p_val}
        
        # Humidity correlation
        if 'RH2M' in self.df.columns:
            corr, p_val = pearsonr(self.df['RH2M'].dropna(), 
                                  self.df.loc[self.df['RH2M'].notna(), 'CASES'])
            results['RH2M'] = {'correlation': corr, 'p_value': p_val}
        
        return results
    
    def spatial_analysis(self):
        """Municipality-level analysis"""
        spatial = self.df.groupby('MUNICIPALITY').agg({
            'CASES': ['sum', 'mean', 'std', 'max'],
            'MORBIDITY_WEEK': 'mean'
        }).round(2)
        return spatial
    
    def risk_stratification(self):
        """Stratify municipalities by risk level"""
        muni_stats = self.spatial_analysis()
        muni_stats.columns = ['_'.join(col).strip() for col in muni_stats.columns.values]
        
        muni_stats['Risk_Level'] = pd.cut(
            muni_stats['CASES_mean'],
            bins=[0, 5, 10, 20, np.inf],
            labels=['Low', 'Moderate', 'High', 'Very High']
        )
        
        return muni_stats.sort_values('CASES_sum', ascending=False)
    
    def outbreak_detection(self, threshold_percentile=75):
        """Identify potential outbreak weeks"""
        threshold = self.df['CASES'].quantile(threshold_percentile / 100)
        outbreaks = self.df[self.df['CASES'] > threshold][
            ['YEAR_2', 'MONTH', 'WEEK', 'MUNICIPALITY', 'CASES']
        ]
        return outbreaks.sort_values('CASES', ascending=False)
    
    def calculate_statistics(self):
        """Generate comprehensive statistics"""
        stats_dict = {
            'Total Cases': self.df['CASES'].sum(),
            'Mean Weekly Cases': self.df['CASES'].mean(),
            'Median Weekly Cases': self.df['CASES'].median(),
            'Std Dev': self.df['CASES'].std(),
            'Min Cases': self.df['CASES'].min(),
            'Max Cases': self.df['CASES'].max(),
            'CV (%)': (self.df['CASES'].std() / self.df['CASES'].mean()) * 100,
        }
        return stats_dict


class ThesisReportGenerator:
    """Generate thesis-ready reports"""
    
    @staticmethod
    def generate_summary(analyzer):
        """Generate statistical summary for thesis"""
        summary = f"""
        DENGUE EPIDEMIOLOGICAL ANALYSIS - SUMMARY STATISTICS
        
        CASE STATISTICS:
        - Total Cases: {analyzer.calculate_statistics()['Total Cases']:.0f}
        - Mean (per week): {analyzer.calculate_statistics()['Mean Weekly Cases']:.2f}
        - Median (per week): {analyzer.calculate_statistics()['Median Weekly Cases']:.2f}
        - Std Deviation: {analyzer.calculate_statistics()['Std Dev']:.2f}
        - Coefficient of Variation: {analyzer.calculate_statistics()['CV (%)']:.2f}%
        - Range: {analyzer.calculate_statistics()['Min Cases']:.0f} - {analyzer.calculate_statistics()['Max Cases']:.0f}
        
        ENVIRONMENTAL CORRELATIONS:
        """
        return summary
    
    @staticmethod
    def export_metrics(analyzer, format='dict'):
        """Export metrics in various formats"""
        metrics = analyzer.calculate_statistics()
        
        if format == 'dict':
            return metrics
        elif format == 'dataframe':
            return pd.DataFrame(metrics, index=[0]).T
        elif format == 'csv':
            df = pd.DataFrame(metrics, index=[0]).T
            return df.to_csv()
        
        return metrics


def quality_assessment(df):
    """Data quality assessment"""
    quality_report = {
        'Total Records': len(df),
        'Missing Values': df.isnull().sum().to_dict(),
        'Duplicate Records': df.duplicated().sum(),
        'Data Completeness (%)': (1 - df.isnull().sum() / len(df) * 100).mean()
    }
    return quality_report
