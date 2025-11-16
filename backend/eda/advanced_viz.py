"""
Advanced Visualizations - Professional, insight-first charts
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

class AdvancedVisualizer:
    """Create professional, annotated visualizations"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        sns.set_style("whitegrid")
        sns.set_palette("husl")
    
    def create_insight_dashboard(self, insights: Dict) -> Dict:
        """Create complete insight dashboard"""
        figures = {
            'quality_scorecard': self.create_quality_scorecard(insights.get('dri', {})),
            'distribution_grid': self.create_distribution_grid(),
            'correlation_network': self.create_correlation_network(),
            'feature_importance': self.create_feature_importance(insights.get('ml_readiness', {}))
        }
        
        return figures
    
    def create_quality_scorecard(self, dri_data: Dict) -> go.Figure:
        """Create DRI scorecard visualization"""
        if not dri_data:
            return None
        
        score = dri_data.get('dri_score', 0)
        components = dri_data.get('component_scores', {})
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Data Reliability Index", 'font': {'size': 24}},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 60], 'color': "lightgray"},
                    {'range': [60, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=400,
            font={'size': 16}
        )
        
        return fig
    
    def create_distribution_grid(self) -> plt.Figure:
        """Create annotated distribution grid"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns[:6]
        
        if len(numeric_cols) == 0:
            return None
        
        n_cols = min(3, len(numeric_cols))
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
        
        for idx, col in enumerate(numeric_cols):
            ax = axes[idx]
            data = self.df[col].dropna()
            
            # Plot distribution
            ax.hist(data, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
            
            # Add statistics annotations
            mean_val = data.mean()
            median_val = data.median()
            
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
            ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
            
            # Add skewness annotation
            skew = data.skew()
            skew_text = f'Skewness: {skew:.2f}'
            if abs(skew) > 1:
                skew_text += '\n(Highly skewed)'
            
            ax.text(0.95, 0.95, skew_text,
                   transform=ax.transAxes,
                   verticalalignment='top',
                   horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            ax.set_title(f'{col}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.legend()
        
        # Hide empty subplots
        for idx in range(len(numeric_cols), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        return fig
    
    def create_correlation_network(self) -> go.Figure:
        """Create interactive correlation network"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return None
        
        corr_matrix = numeric_df.corr()
        
        # Create heatmap with annotations
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title='Correlation Heatmap',
            xaxis_title='Features',
            yaxis_title='Features',
            height=600,
            width=800
        )
        
        return fig
    
    def create_feature_importance(self, ml_data: Dict) -> plt.Figure:
        """Create feature importance chart"""
        feature_scores = ml_data.get('feature_scores', {})
        
        if not feature_scores or 'top_features' not in feature_scores:
            return None
        
        top_features = feature_scores['top_features'][:10]
        
        if not top_features:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        features = [f['feature'] for f in top_features]
        scores = [f['score'] for f in top_features]
        colors = ['steelblue' if f['type'] == 'numeric' else 'coral' for f in top_features]
        
        bars = ax.barh(features, scores, color=colors)
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score, i, f' {score:.3f}', va='center')
        
        ax.set_xlabel('Feature Importance Score', fontsize=12)
        ax.set_title('Top 10 Most Important Features', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='steelblue', label='Numeric'),
            Patch(facecolor='coral', label='Categorical')
        ]
        ax.legend(handles=legend_elements, loc='lower right')
        
        plt.tight_layout()
        return fig
    
    def create_pareto_chart(self, col: str) -> plt.Figure:
        """Create Pareto chart for categorical data"""
        if col not in self.df.columns:
            return None
        
        value_counts = self.df[col].value_counts()
        
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Bar chart
        ax1.bar(range(len(value_counts)), value_counts.values, color='steelblue', alpha=0.7)
        ax1.set_xlabel('Categories', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12, color='steelblue')
        ax1.tick_params(axis='y', labelcolor='steelblue')
        
        # Cumulative line
        ax2 = ax1.twinx()
        cumsum = value_counts.cumsum() / value_counts.sum() * 100
        ax2.plot(range(len(cumsum)), cumsum.values, color='red', marker='o', linewidth=2)
        ax2.set_ylabel('Cumulative Percentage', fontsize=12, color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.axhline(80, color='green', linestyle='--', label='80% threshold')
        
        # Add 80/20 annotation
        idx_80 = (cumsum >= 80).idxmax() if (cumsum >= 80).any() else len(cumsum) - 1
        ax2.annotate(f'80% at category {idx_80}',
                    xy=(idx_80, 80),
                    xytext=(idx_80 + 1, 70),
                    arrowprops=dict(arrowstyle='->', color='green'))
        
        plt.title(f'Pareto Chart: {col}', fontsize=14, fontweight='bold')
        ax2.legend()
        plt.tight_layout()
        
        return fig
    
    def create_comparison_chart(self, col: str, target_col: str) -> plt.Figure:
        """Create comparison chart between groups"""
        if col not in self.df.columns or target_col not in self.df.columns:
            return None
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Split by target
        target_unique = self.df[target_col].unique()[:2]  # Top 2 classes
        
        for idx, target_val in enumerate(target_unique):
            ax = axes[idx]
            data = self.df[self.df[target_col] == target_val][col].dropna()
            
            ax.hist(data, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
            ax.set_title(f'{col} when {target_col}={target_val}', fontweight='bold')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            
            # Add statistics
            mean_val = data.mean()
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2)
            ax.text(0.95, 0.95, f'Mean: {mean_val:.2f}\nCount: {len(data)}',
                   transform=ax.transAxes,
                   verticalalignment='top',
                   horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        return fig
    
    def create_missing_data_matrix(self) -> plt.Figure:
        """Create missing data matrix visualization"""
        missing = self.df.isnull()
        
        if missing.sum().sum() == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create matrix
        sns.heatmap(missing, cbar=True, cmap='YlOrRd', ax=ax, yticklabels=False)
        
        ax.set_title('Missing Data Pattern', fontsize=14, fontweight='bold')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Rows')
        
        # Add summary text
        total_missing = missing.sum().sum()
        total_cells = missing.size
        missing_pct = (total_missing / total_cells) * 100
        
        ax.text(0.5, -0.1, f'Total Missing: {total_missing:,} ({missing_pct:.2f}%)',
               transform=ax.transAxes,
               ha='center',
               fontsize=12,
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        plt.tight_layout()
        return fig
    
    def create_outlier_boxplot_grid(self) -> plt.Figure:
        """Create grid of boxplots with outlier annotations"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns[:6]
        
        if len(numeric_cols) == 0:
            return None
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        for idx, col in enumerate(numeric_cols):
            ax = axes[idx]
            data = self.df[col].dropna()
            
            # Create boxplot
            bp = ax.boxplot(data, vert=True, patch_artist=True)
            bp['boxes'][0].set_facecolor('lightblue')
            
            # Calculate outliers
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[(data < Q1 - 1.5*IQR) | (data > Q3 + 1.5*IQR)]
            
            # Add annotations
            outlier_pct = len(outliers) / len(data) * 100
            ax.set_title(f'{col}', fontweight='bold')
            ax.text(0.5, 0.95, f'Outliers: {len(outliers)} ({outlier_pct:.1f}%)',
                   transform=ax.transAxes,
                   ha='center',
                   va='top',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        # Hide empty subplots
        for idx in range(len(numeric_cols), len(axes)):
            axes[idx].axis('off')
        
        plt.suptitle('Outlier Detection - Box Plots', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    def create_storytelling_sequence(self, insights: Dict) -> List[plt.Figure]:
        """Create sequence of charts that tell a story"""
        figures = []
        
        # 1. Data Quality Overview
        fig1 = self.create_quality_overview(insights)
        if fig1:
            figures.append(('Data Quality Overview', fig1))
        
        # 2. Key Distributions
        fig2 = self.create_distribution_grid()
        if fig2:
            figures.append(('Feature Distributions', fig2))
        
        # 3. Relationships
        fig3 = self.create_correlation_network()
        if fig3:
            figures.append(('Feature Relationships', fig3))
        
        # 4. Recommendations
        fig4 = self.create_recommendations_summary(insights)
        if fig4:
            figures.append(('Recommendations', fig4))
        
        return figures
    
    def create_quality_overview(self, insights: Dict) -> plt.Figure:
        """Create quality overview chart"""
        dri_data = insights.get('dri', {})
        components = dri_data.get('component_scores', {})
        
        if not components:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = list(components.keys())
        scores = list(components.values())
        
        bars = ax.barh(categories, scores, color=['green' if s >= 80 else 'orange' if s >= 60 else 'red' for s in scores])
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score + 2, i, f'{score:.0f}', va='center')
        
        ax.set_xlabel('Score (0-100)', fontsize=12)
        ax.set_title('Data Quality Components', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 110)
        ax.axvline(80, color='green', linestyle='--', alpha=0.5, label='Good threshold')
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    def create_recommendations_summary(self, insights: Dict) -> plt.Figure:
        """Create recommendations summary"""
        ml_data = insights.get('ml_readiness', {})
        transforms = ml_data.get('transform_recommendations', {})
        
        if not transforms:
            return None
        
        # Count recommendation types
        rec_counts = {}
        for col, rec_data in transforms.items():
            for rec in rec_data.get('recommended', []):
                rec_counts[rec] = rec_counts.get(rec, 0) + 1
        
        if not rec_counts:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        recs = list(rec_counts.keys())
        counts = list(rec_counts.values())
        
        bars = ax.bar(recs, counts, color='steelblue', alpha=0.7)
        
        # Add value labels
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count)}',
                   ha='center', va='bottom')
        
        ax.set_ylabel('Number of Features', fontsize=12)
        ax.set_title('Recommended Transformations', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig
