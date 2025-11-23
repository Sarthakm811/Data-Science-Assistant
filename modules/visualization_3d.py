"""3D Visualization Module"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.decomposition import PCA

class Visualizer3D:
    def __init__(self, df):
        self.df = df
    
    def scatter_3d(self, x_col, y_col, z_col, color_col=None, size_col=None):
        """Create 3D scatter plot"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        fig = px.scatter_3d(
            self.df,
            x=x_col,
            y=y_col,
            z=z_col,
            color=color_col,
            size=size_col,
            hover_data=self.df.columns,
            title=f'3D Scatter: {x_col} vs {y_col} vs {z_col}'
        )
        fig.update_layout(height=700)
        return fig
    
    def surface_plot(self, x_col, y_col, z_col):
        """Create 3D surface plot"""
        try:
            # Try to create pivot table with binning for continuous data
            df_temp = self.df[[x_col, y_col, z_col]].dropna()
            
            # Bin the continuous variables to create a grid
            x_bins = pd.cut(df_temp[x_col], bins=10)
            y_bins = pd.cut(df_temp[y_col], bins=10)
            
            pivot_data = df_temp.groupby([y_bins, x_bins])[z_col].mean().unstack()
            
            fig = go.Figure(data=[go.Surface(
                z=pivot_data.values,
                x=range(len(pivot_data.columns)),
                y=range(len(pivot_data.index))
            )])
            fig.update_layout(
                title=f'3D Surface: {z_col}',
                height=700,
                scene=dict(
                    xaxis_title=x_col,
                    yaxis_title=y_col,
                    zaxis_title=z_col
                )
            )
            return fig
        except Exception as e:
            # Fallback: use scatter plot instead
            fig = go.Figure(data=[go.Scatter3d(
                x=self.df[x_col],
                y=self.df[y_col],
                z=self.df[z_col],
                mode='markers',
                marker=dict(size=4, color=self.df[z_col], colorscale='Viridis')
            )])
            fig.update_layout(
                title=f'3D Scatter (Surface unavailable): {z_col}',
                height=700,
                scene=dict(
                    xaxis_title=x_col,
                    yaxis_title=y_col,
                    zaxis_title=z_col
                )
            )
            return fig
    
    def pca_3d(self):
        """3D PCA visualization"""
        numeric_df = self.df.select_dtypes(include=[np.number]).dropna()
        
        if numeric_df.shape[1] < 3:
            return None, "Need at least 3 numeric columns"
        
        pca = PCA(n_components=3)
        components = pca.fit_transform(numeric_df)
        
        fig = px.scatter_3d(
            x=components[:, 0],
            y=components[:, 1],
            z=components[:, 2],
            labels={
                'x': f'PC1 ({pca.explained_variance_ratio_[0]:.2%})',
                'y': f'PC2 ({pca.explained_variance_ratio_[1]:.2%})',
                'z': f'PC3 ({pca.explained_variance_ratio_[2]:.2%})'
            },
            title='3D PCA Visualization'
        )
        fig.update_layout(height=700)
        return fig, pca.explained_variance_ratio_
    
    def bubble_3d(self, x_col, y_col, z_col, size_col, color_col=None):
        """Create 3D bubble chart"""
        fig = px.scatter_3d(
            self.df,
            x=x_col,
            y=y_col,
            z=z_col,
            size=size_col,
            color=color_col,
            hover_name=self.df.index,
            title='3D Bubble Chart'
        )
        fig.update_layout(height=700)
        return fig
