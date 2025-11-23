"""Anomaly Detection Module"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from scipy import stats

class AnomalyDetector:
    def __init__(self, df):
        self.df = df
    
    def isolation_forest(self, contamination=0.1):
        """Detect anomalies using Isolation Forest"""
        numeric_df = self.df.select_dtypes(include=[np.number]).dropna()
        
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_df)
        
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        anomalies = iso_forest.fit_predict(scaled_data)
        
        self.df['anomaly'] = 'Normal'
        self.df.loc[numeric_df.index[anomalies == -1], 'anomaly'] = 'Anomaly'
        
        return self.df, anomalies
    
    def statistical_anomalies(self, method='zscore', threshold=3):
        """Detect anomalies using statistical methods"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if method == 'zscore':
            z_scores = np.abs(stats.zscore(numeric_df.dropna()))
            anomalies = (z_scores > threshold).any(axis=1)
        elif method == 'iqr':
            Q1 = numeric_df.quantile(0.25)
            Q3 = numeric_df.quantile(0.75)
            IQR = Q3 - Q1
            anomalies = ((numeric_df < (Q1 - 1.5 * IQR)) | (numeric_df > (Q3 + 1.5 * IQR))).any(axis=1)
        
        self.df['anomaly'] = 'Normal'
        self.df.loc[anomalies, 'anomaly'] = 'Anomaly'
        
        return self.df, anomalies
    
    def visualize_anomalies(self, x_col, y_col):
        """Visualize anomalies"""
        fig = go.Figure()
        
        normal = self.df[self.df['anomaly'] == 'Normal']
        anomalies = self.df[self.df['anomaly'] == 'Anomaly']
        
        fig.add_trace(go.Scatter(
            x=normal[x_col],
            y=normal[y_col],
            mode='markers',
            name='Normal',
            marker=dict(size=8, color='blue')
        ))
        
        fig.add_trace(go.Scatter(
            x=anomalies[x_col],
            y=anomalies[y_col],
            mode='markers',
            name='Anomaly',
            marker=dict(size=10, color='red', symbol='x')
        ))
        
        fig.update_layout(
            title='Anomaly Detection',
            xaxis_title=x_col,
            yaxis_title=y_col,
            height=600
        )
        
        return fig
    
    def get_anomaly_summary(self):
        """Get anomaly summary statistics"""
        if 'anomaly' not in self.df.columns:
            return None
        
        summary = self.df['anomaly'].value_counts()
        percentage = (summary / len(self.df) * 100).round(2)
        
        return pd.DataFrame({
            'Count': summary,
            'Percentage': percentage
        })
