"""Time Series Forecasting Module"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.seasonal import seasonal_decompose
    STATSMODELS_AVAILABLE = True
except:
    STATSMODELS_AVAILABLE = False

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except:
    PROPHET_AVAILABLE = False

class TimeSeriesForecaster:
    def __init__(self, df, date_col, value_col):
        self.df = df.copy()
        self.date_col = date_col
        self.value_col = value_col
        self.df[date_col] = pd.to_datetime(self.df[date_col])
        self.df = self.df.sort_values(date_col)
    
    def decompose_series(self):
        """Decompose time series"""
        if not STATSMODELS_AVAILABLE:
            return None, "Statsmodels not available"
        
        try:
            ts_data = self.df.set_index(self.date_col)[self.value_col]
            decomposition = seasonal_decompose(ts_data, model='additive', period=12)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=decomposition.trend, name='Trend'))
            fig.add_trace(go.Scatter(y=decomposition.seasonal, name='Seasonal'))
            fig.add_trace(go.Scatter(y=decomposition.resid, name='Residual'))
            
            fig.update_layout(title='Time Series Decomposition', height=600)
            return fig, decomposition
        except Exception as e:
            return None, str(e)
    
    def arima_forecast(self, order=(1, 1, 1), periods=30):
        """ARIMA forecasting"""
        if not STATSMODELS_AVAILABLE:
            return None, "Statsmodels not available"
        
        try:
            ts_data = self.df.set_index(self.date_col)[self.value_col]
            model = ARIMA(ts_data, order=order)
            results = model.fit()
            
            forecast = results.get_forecast(steps=periods)
            forecast_df = forecast.conf_int(alpha=0.05)
            forecast_df['forecast'] = forecast.predicted_mean
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=ts_data.index,
                y=ts_data.values,
                name='Historical',
                mode='lines'
            ))
            
            future_dates = pd.date_range(ts_data.index[-1], periods=periods+1)[1:]
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=forecast_df['forecast'],
                name='Forecast',
                mode='lines',
                line=dict(dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=forecast_df.iloc[:, 0],
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=forecast_df.iloc[:, 1],
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,0,0,0)',
                name='95% CI'
            ))
            
            fig.update_layout(title='ARIMA Forecast', height=600)
            return fig, results.summary()
        except Exception as e:
            return None, str(e)
    
    def prophet_forecast(self, periods=30):
        """Prophet forecasting"""
        if not PROPHET_AVAILABLE:
            return None, "Prophet not available"
        
        try:
            prophet_df = self.df[[self.date_col, self.value_col]].copy()
            prophet_df.columns = ['ds', 'y']
            
            model = Prophet(yearly_seasonality=True, daily_seasonality=False)
            model.fit(prophet_df)
            
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=prophet_df['ds'],
                y=prophet_df['y'],
                name='Historical',
                mode='lines'
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat'],
                name='Forecast',
                mode='lines',
                line=dict(dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_upper'],
                fill=None,
                mode='lines',
                line_color='rgba(0,0,0,0)',
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast['ds'],
                y=forecast['yhat_lower'],
                fill='tonexty',
                mode='lines',
                line_color='rgba(0,0,0,0)',
                name='95% CI'
            ))
            
            fig.update_layout(title='Prophet Forecast', height=600)
            return fig, forecast
        except Exception as e:
            return None, str(e)
