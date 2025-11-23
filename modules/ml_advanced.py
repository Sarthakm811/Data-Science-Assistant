"""Advanced Machine Learning Module"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.metrics import (
    confusion_matrix, roc_curve, auc, classification_report,
    mean_squared_error, r2_score, mean_absolute_error
)
import warnings
warnings.filterwarnings('ignore')

class AdvancedML:
    def __init__(self, X_train, X_test, y_train, y_test, task='classification'):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.task = task
        self.models = {}
    
    def feature_importance(self, model, feature_names):
        """Get feature importance"""
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            
            fig = px.bar(
                x=importance,
                y=feature_names,
                orientation='h',
                title='Feature Importance',
                labels={'x': 'Importance', 'y': 'Features'}
            )
            fig.update_layout(height=600)
            return fig
        return None
    
    def hyperparameter_tuning(self, model, param_grid, method='grid', cv=5):
        """Hyperparameter tuning"""
        if method == 'grid':
            search = GridSearchCV(model, param_grid, cv=cv, n_jobs=-1)
        else:
            search = RandomizedSearchCV(model, param_grid, cv=cv, n_jobs=-1)
        
        search.fit(self.X_train, self.y_train)
        
        results_df = pd.DataFrame(search.cv_results_)
        return search.best_model_, search.best_params_, results_df
    
    def cross_validation(self, model, cv=5):
        """Cross-validation analysis"""
        scores = cross_val_score(model, self.X_train, self.y_train, cv=cv)
        
        fig = go.Figure()
        fig.add_trace(go.Box(y=scores, name='CV Scores'))
        fig.update_layout(
            title=f'Cross-Validation Scores (Mean: {scores.mean():.4f})',
            yaxis_title='Score',
            height=400
        )
        
        return fig, scores
    
    def confusion_matrix_plot(self, y_pred):
        """Plot confusion matrix"""
        cm = confusion_matrix(self.y_test, y_pred)
        
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Predicted Negative', 'Predicted Positive'],
            y=['Actual Negative', 'Actual Positive'],
            text=cm,
            texttemplate='%{text}',
            colorscale='Blues'
        ))
        fig.update_layout(title='Confusion Matrix', height=500)
        return fig
    
    def roc_curve_plot(self, y_pred_proba):
        """Plot ROC curve"""
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f'ROC (AUC={roc_auc:.3f})'))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], name='Random', line=dict(dash='dash')))
        
        fig.update_layout(
            title='ROC Curve',
            xaxis_title='False Positive Rate',
            yaxis_title='True Positive Rate',
            height=600
        )
        return fig, roc_auc
    
    def model_comparison(self, models_dict):
        """Compare multiple models"""
        results = []
        
        for name, model in models_dict.items():
            model.fit(self.X_train, self.y_train)
            y_pred = model.predict(self.X_test)
            
            if self.task == 'classification':
                score = model.score(self.X_test, self.y_test)
                results.append({'Model': name, 'Accuracy': score})
            else:
                r2 = r2_score(self.y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
                results.append({'Model': name, 'R2': r2, 'RMSE': rmse})
        
        results_df = pd.DataFrame(results)
        
        fig = px.bar(results_df, x='Model', y=results_df.columns[1:], barmode='group')
        fig.update_layout(height=500)
        
        return results_df, fig
    
    def classification_report_plot(self, y_pred):
        """Generate classification report"""
        report = classification_report(self.y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        return report_df
