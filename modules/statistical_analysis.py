"""Advanced Statistical Analysis Module"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import shapiro, normaltest, anderson, kstest
import plotly.graph_objects as go
import plotly.express as px

class StatisticalAnalyzer:
    def __init__(self, df):
        self.df = df
    
    def normality_tests(self):
        """Perform normality tests on numeric columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        results = {}
        
        for col in numeric_cols:
            data = self.df[col].dropna()
            if len(data) > 3:
                results[col] = {
                    'Shapiro-Wilk': shapiro(data)[1],
                    'Kolmogorov-Smirnov': kstest(data, 'norm')[1],
                    'Anderson-Darling': anderson(data)[1]
                }
        return results
    
    def distribution_analysis(self, column):
        """Analyze distribution of a column"""
        data = self.df[column].dropna()
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=data, nbinsx=30, name='Histogram'))
        fig.add_trace(go.Box(x=data, name='Box Plot', yaxis='y2'))
        
        fig.update_layout(
            title=f'Distribution Analysis: {column}',
            xaxis_title=column,
            yaxis_title='Frequency',
            yaxis2=dict(title='Box Plot', overlaying='y', side='right'),
            hovermode='x unified'
        )
        return fig
    
    def hypothesis_testing(self, col1, col2, test_type='ttest'):
        """Perform hypothesis tests"""
        data1 = self.df[col1].dropna()
        data2 = self.df[col2].dropna()
        
        if test_type == 'ttest':
            stat, pvalue = stats.ttest_ind(data1, data2)
            return {'test': 't-test', 'statistic': stat, 'p-value': pvalue}
        elif test_type == 'mannwhitney':
            stat, pvalue = stats.mannwhitneyu(data1, data2)
            return {'test': 'Mann-Whitney U', 'statistic': stat, 'p-value': pvalue}
        elif test_type == 'ks':
            stat, pvalue = stats.ks_2samp(data1, data2)
            return {'test': 'Kolmogorov-Smirnov', 'statistic': stat, 'p-value': pvalue}
    
    def correlation_analysis(self):
        """Analyze correlations"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0
        ))
        fig.update_layout(title='Correlation Matrix', height=600)
        return fig, corr_matrix
    
    def descriptive_stats(self):
        """Get descriptive statistics"""
        return self.df.describe().T
