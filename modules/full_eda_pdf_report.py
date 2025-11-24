"""Full EDA PDF Report with ALL Charts, Graphs, Dashboards and Insights"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

class FullEDAPDFReport:
    def __init__(self, df, dataset_name="Dataset"):
        self.df = df
        self.dataset_name = dataset_name
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.buffer = io.BytesIO()
        self.story = []
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
    
    def _img_to_bytes(self, fig):
        """Convert matplotlib figure to bytes"""
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        return img_buffer
    
    def _create_title_page(self):
        """Create title page"""
        self.story.append(Spacer(1, 2*inch))
        title = Paragraph("📊 FULL EDA REPORT WITH ALL VISUALIZATIONS", self.styles['CustomTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.3*inch))
        
        subtitle = Paragraph(
            f"<b>Dataset:</b> {self.dataset_name}<br/>"
            f"<b>Generated:</b> {self.timestamp}<br/>"
            f"<b>Rows:</b> {self.df.shape[0]} | <b>Columns:</b> {self.df.shape[1]}",
            self.styles['Normal']
        )
        self.story.append(subtitle)
        self.story.append(PageBreak())
    
    def _add_missing_data_visualization(self):
        """Add missing data charts"""
        self.story.append(Paragraph("1. MISSING DATA VISUALIZATION", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100)
        
        if missing.sum() > 0:
            # Missing data bar chart
            fig, ax = plt.subplots(figsize=(10, 5))
            missing_data = missing[missing > 0].sort_values(ascending=False)
            missing_data.plot(kind='barh', ax=ax, color='coral')
            ax.set_title('Missing Data Count by Column', fontsize=14, fontweight='bold')
            ax.set_xlabel('Number of Missing Values')
            
            img = Image(self._img_to_bytes(fig), width=5.5*inch, height=3*inch)
            self.story.append(img)
            self.story.append(Spacer(1, 0.2*inch))
            
            # Missing data percentage chart
            fig, ax = plt.subplots(figsize=(10, 5))
            missing_pct_data = missing_pct[missing_pct > 0].sort_values(ascending=False)
            missing_pct_data.plot(kind='barh', ax=ax, color='lightcoral')
            ax.set_title('Missing Data Percentage by Column', fontsize=14, fontweight='bold')
            ax.set_xlabel('Percentage Missing (%)')
            
            img = Image(self._img_to_bytes(fig), width=5.5*inch, height=3*inch)
            self.story.append(img)
        else:
            self.story.append(Paragraph("✅ No missing data found!", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_distribution_charts(self):
        """Add distribution charts for ALL numeric columns"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("2. DISTRIBUTION ANALYSIS - ALL NUMERIC COLUMNS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            try:
                # Create figure with histogram and KDE
                fig, axes = plt.subplots(1, 2, figsize=(12, 4))
                
                # Histogram
                axes[0].hist(self.df[col].dropna(), bins=30, edgecolor='black', alpha=0.7, color='steelblue')
                axes[0].set_title(f'Histogram: {col}', fontweight='bold')
                axes[0].set_xlabel(col)
                axes[0].set_ylabel('Frequency')
                axes[0].grid(alpha=0.3)
                
                # KDE plot
                self.df[col].dropna().plot(kind='kde', ax=axes[1], color='darkblue', linewidth=2)
                axes[1].set_title(f'KDE Plot: {col}', fontweight='bold')
                axes[1].set_xlabel(col)
                axes[1].grid(alpha=0.3)
                
                plt.tight_layout()
                img = Image(self._img_to_bytes(fig), width=5.5*inch, height=2.5*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 0.15*inch))
            except:
                pass
    
    def _add_box_plots(self):
        """Add box plots for outlier visualization"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("3. BOX PLOTS - OUTLIER DETECTION", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Create subplots for box plots
        n_cols = len(numeric_cols)
        n_rows = (n_cols + 2) // 3
        
        fig, axes = plt.subplots(n_rows, 3, figsize=(14, 4*n_rows))
        axes = axes.flatten()
        
        for idx, col in enumerate(numeric_cols):
            axes[idx].boxplot(self.df[col].dropna(), vert=True)
            axes[idx].set_title(f'Box Plot: {col}', fontweight='bold')
            axes[idx].set_ylabel(col)
            axes[idx].grid(alpha=0.3)
        
        # Hide empty subplots
        for idx in range(len(numeric_cols), len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        img = Image(self._img_to_bytes(fig), width=5.5*inch, height=4*n_rows*inch)
        self.story.append(img)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_correlation_heatmap(self):
        """Add correlation heatmap"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("4. CORRELATION HEATMAP", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            corr_matrix = numeric_df.corr()
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, 
                       cbar_kws={'label': 'Correlation'}, square=True)
            ax.set_title('Correlation Matrix - All Numeric Columns', fontsize=14, fontweight='bold')
            
            img = Image(self._img_to_bytes(fig), width=5.5*inch, height=5*inch)
            self.story.append(img)
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_categorical_charts(self):
        """Add categorical variable charts"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("5. CATEGORICAL VARIABLES ANALYSIS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        cat_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(cat_cols) > 0:
            for col in cat_cols:
                try:
                    fig, ax = plt.subplots(figsize=(10, 5))
                    value_counts = self.df[col].value_counts().head(15)
                    value_counts.plot(kind='barh', ax=ax, color='steelblue')
                    ax.set_title(f'Value Counts: {col} (Top 15)', fontsize=12, fontweight='bold')
                    ax.set_xlabel('Count')
                    ax.grid(alpha=0.3, axis='x')
                    
                    img = Image(self._img_to_bytes(fig), width=5.5*inch, height=3*inch)
                    self.story.append(img)
                    self.story.append(Spacer(1, 0.2*inch))
                except (ValueError, OSError, RuntimeError) as e:
                    import logging
                    logging.debug(f"Failed to generate bar chart for {col}: {e}")
        else:
            self.story.append(Paragraph("No categorical variables found", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_pairplot(self):
        """Add pairplot for relationships"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("6. PAIRPLOT - RELATIONSHIPS BETWEEN VARIABLES", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 2:
            try:
                # Limit to first 4 columns to avoid huge plot
                subset_cols = numeric_cols[:4]
                pairgrid = sns.pairplot(self.df[subset_cols], diag_kind='hist', plot_kws={'alpha': 0.6})
                
                img_buffer = io.BytesIO()
                pairgrid.fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close('all')
                
                img = Image(img_buffer, width=5.5*inch, height=5.5*inch)
                self.story.append(img)
            except (ValueError, OSError, RuntimeError, AttributeError) as e:
                import logging
                logging.debug(f"Failed to generate pairplot: {e}")
                self.story.append(Paragraph("Could not generate pairplot", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_distribution_comparison(self):
        """Add distribution comparison plots"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("7. DISTRIBUTION COMPARISON - VIOLIN & DENSITY PLOTS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:4]:  # Limit to first 4
            try:
                fig, axes = plt.subplots(1, 2, figsize=(12, 4))
                
                # Violin plot
                axes[0].violinplot(self.df[col].dropna(), vert=True)
                axes[0].set_title(f'Violin Plot: {col}', fontweight='bold')
                axes[0].set_ylabel(col)
                axes[0].grid(alpha=0.3)
                
                # Density plot
                self.df[col].dropna().plot(kind='density', ax=axes[1], color='darkblue', linewidth=2)
                axes[1].fill_between(axes[1].get_lines()[0].get_xdata(), 
                                     axes[1].get_lines()[0].get_ydata(), alpha=0.3)
                axes[1].set_title(f'Density Plot: {col}', fontweight='bold')
                axes[1].grid(alpha=0.3)
                
                plt.tight_layout()
                img = Image(self._img_to_bytes(fig), width=5.5*inch, height=2.5*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 0.15*inch))
            except (ValueError, OSError, RuntimeError, IndexError) as e:
                import logging
                logging.debug(f"Failed to add distribution plot for {col}: {e}")
    
    def _add_statistical_summary_charts(self):
        """Add statistical summary charts"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("8. STATISTICAL SUMMARY", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Skewness chart
        fig, ax = plt.subplots(figsize=(10, 5))
        skewness_values = [self.df[col].skew() for col in numeric_cols]
        ax.barh(range(len(numeric_cols)), skewness_values, color='steelblue')
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_yticklabels(numeric_cols)
        ax.set_title('Skewness by Column', fontsize=12, fontweight='bold')
        ax.set_xlabel('Skewness')
        ax.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax.grid(alpha=0.3, axis='x')
        
        img = Image(self._img_to_bytes(fig), width=5.5*inch, height=3*inch)
        self.story.append(img)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Kurtosis chart
        fig, ax = plt.subplots(figsize=(10, 5))
        kurtosis_values = [self.df[col].kurtosis() for col in numeric_cols]
        ax.barh(range(len(numeric_cols)), kurtosis_values, color='coral')
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_yticklabels(numeric_cols)
        ax.set_title('Kurtosis by Column', fontsize=12, fontweight='bold')
        ax.set_xlabel('Kurtosis')
        ax.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax.grid(alpha=0.3, axis='x')
        
        img = Image(self._img_to_bytes(fig), width=5.5*inch, height=3*inch)
        self.story.append(img)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_data_type_summary(self):
        """Add data type summary chart"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("9. DATA TYPE SUMMARY", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        dtype_counts = self.df.dtypes.value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        dtype_counts.plot(kind='bar', ax=ax, color='steelblue')
        ax.set_title('Data Types Distribution', fontsize=12, fontweight='bold')
        ax.set_xlabel('Data Type')
        ax.set_ylabel('Count')
        ax.grid(alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')
        
        img = Image(self._img_to_bytes(fig), width=5.5*inch, height=3*inch)
        self.story.append(img)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_summary_statistics(self):
        """Add summary statistics table"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("10. SUMMARY STATISTICS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        stats_summary = numeric_df.describe().round(4)
        
        data = [['Statistic'] + list(stats_summary.columns[:5])]  # Limit to first 5 columns
        for idx, row in stats_summary.iterrows():
            data.append([str(idx)] + [f"{val:.4f}" if isinstance(val, float) else str(val) for val in row[:5]])
        
        table = Table(data, colWidths=[1.2*inch] + [0.8*inch] * 5)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_outlier_analysis(self):
        """Add comprehensive outlier analysis and detection"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("11. OUTLIER ANALYSIS & DETECTION", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outlier_summary = []
        
        for col in numeric_cols:
            try:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)][col]
                outlier_count = len(outliers)
                outlier_pct = (outlier_count / len(self.df)) * 100
                
                if outlier_count > 0:
                    outlier_summary.append([col, str(outlier_count), f"{outlier_pct:.2f}%", f"{lower_bound:.2f}", f"{upper_bound:.2f}"])
            except:
                pass
        
        if outlier_summary:
            # Outlier summary table
            data = [['Column', 'Outlier Count', 'Percentage', 'Lower Bound', 'Upper Bound']]
            data.extend(outlier_summary)
            
            table = Table(data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            self.story.append(table)
            self.story.append(Spacer(1, 0.3*inch))
            
            # Outlier visualization
            fig, axes = plt.subplots(min(3, len(numeric_cols)), 1, figsize=(10, 4*min(3, len(numeric_cols))))
            if len(numeric_cols) == 1:
                axes = [axes]
            
            for idx, col in enumerate(numeric_cols[:3]):
                try:
                    axes[idx].scatter(range(len(self.df)), self.df[col], alpha=0.6, s=30)
                    axes[idx].set_title(f'Outlier Detection: {col}', fontweight='bold')
                    axes[idx].set_ylabel(col)
                    axes[idx].grid(alpha=0.3)
                except:
                    pass
            
            plt.tight_layout()
            img = Image(self._img_to_bytes(fig), width=5.5*inch, height=3*min(3, len(numeric_cols))*inch)
            self.story.append(img)
        else:
            self.story.append(Paragraph("✅ No significant outliers detected", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_feature_correlation_insights(self):
        """Add detailed feature correlation insights"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("12. FEATURE CORRELATION INSIGHTS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            
            # Find strong correlations
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        strong_corr.append([
                            corr_matrix.columns[i],
                            corr_matrix.columns[j],
                            f"{corr_val:.4f}"
                        ])
            
            if strong_corr:
                self.story.append(Paragraph("<b>Strong Correlations (|r| > 0.7):</b>", self.styles['Normal']))
                data = [['Feature 1', 'Feature 2', 'Correlation']]
                data.extend(strong_corr)
                
                table = Table(data, colWidths=[2*inch, 2*inch, 1.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                ]))
                self.story.append(table)
                self.story.append(Spacer(1, 0.2*inch))
            
            # Scatter plots for strong correlations
            if len(strong_corr) > 0:
                for idx, (feat1, feat2, corr_val) in enumerate(strong_corr[:4]):
                    try:
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.scatter(self.df[feat1], self.df[feat2], alpha=0.6, s=50)
                        
                        # Add trend line
                        z = np.polyfit(self.df[feat1].dropna(), self.df[feat2].dropna(), 1)
                        p = np.poly1d(z)
                        ax.plot(self.df[feat1].sort_values(), p(self.df[feat1].sort_values()), "r--", linewidth=2, label='Trend')
                        
                        ax.set_xlabel(feat1, fontweight='bold')
                        ax.set_ylabel(feat2, fontweight='bold')
                        ax.set_title(f'Correlation: {feat1} vs {feat2} (r={corr_val})', fontweight='bold')
                        ax.grid(alpha=0.3)
                        ax.legend()
                        
                        img = Image(self._img_to_bytes(fig), width=5.5*inch, height=3*inch)
                        self.story.append(img)
                        self.story.append(Spacer(1, 0.15*inch))
                    except:
                        pass
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_normality_tests(self):
        """Add normality tests and Q-Q plots"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("13. NORMALITY ANALYSIS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        normality_results = []
        
        for col in numeric_cols:
            try:
                stat, p_value = stats.shapiro(self.df[col].dropna()[:5000])  # Limit to 5000 samples
                is_normal = "Yes" if p_value > 0.05 else "No"
                normality_results.append([col, f"{p_value:.6f}", is_normal])
            except:
                pass
        
        if normality_results:
            self.story.append(Paragraph("<b>Shapiro-Wilk Normality Test Results:</b>", self.styles['Normal']))
            data = [['Column', 'P-Value', 'Normal (p>0.05)?']]
            data.extend(normality_results)
            
            table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            self.story.append(table)
            self.story.append(Spacer(1, 0.2*inch))
        
        # Q-Q plots
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        for idx, col in enumerate(numeric_cols[:4]):
            try:
                stats.probplot(self.df[col].dropna(), dist="norm", plot=axes[idx])
                axes[idx].set_title(f'Q-Q Plot: {col}', fontweight='bold')
            except:
                axes[idx].axis('off')
        
        plt.tight_layout()
        img = Image(self._img_to_bytes(fig), width=5.5*inch, height=5*inch)
        self.story.append(img)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_feature_distribution_matrix(self):
        """Add feature distribution comparison matrix"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("14. FEATURE DISTRIBUTION MATRIX", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 2:
            try:
                n_features = min(5, len(numeric_cols))
                pairgrid = sns.pairplot(self.df[numeric_cols[:n_features]], 
                                  diag_kind='kde', 
                                  plot_kws={'alpha': 0.6, 's': 30},
                                  diag_kws={'linewidth': 2})
                
                img_buffer = io.BytesIO()
                pairgrid.fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close('all')
                
                img = Image(img_buffer, width=6*inch, height=6*inch)
                self.story.append(img)
            except:
                self.story.append(Paragraph("Could not generate feature distribution matrix", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_categorical_insights(self):
        """Add categorical variable insights and patterns"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("15. CATEGORICAL VARIABLE INSIGHTS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        cat_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(cat_cols) > 0:
            for col in cat_cols[:5]:  # Limit to first 5
                try:
                    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
                    
                    # Value counts bar chart
                    value_counts = self.df[col].value_counts().head(15)
                    value_counts.plot(kind='bar', ax=axes[0], color='steelblue')
                    axes[0].set_title(f'Top Values: {col}', fontweight='bold')
                    axes[0].set_xlabel('Category')
                    axes[0].set_ylabel('Count')
                    axes[0].tick_params(axis='x', rotation=45)
                    axes[0].grid(alpha=0.3, axis='y')
                    
                    # Pie chart
                    axes[1].pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
                    axes[1].set_title(f'Distribution: {col}', fontweight='bold')
                    
                    plt.tight_layout()
                    img = Image(self._img_to_bytes(fig), width=5.5*inch, height=3*inch)
                    self.story.append(img)
                    self.story.append(Spacer(1, 0.15*inch))
                except:
                    pass
        else:
            self.story.append(Paragraph("No categorical variables found", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_data_quality_dashboard(self):
        """Add comprehensive data quality dashboard"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("16. DATA QUALITY DASHBOARD", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Calculate quality metrics
        total_cells = self.df.shape[0] * self.df.shape[1]
        missing_cells = self.df.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells * 100)
        
        duplicate_rows = self.df.duplicated().sum()
        duplicate_pct = (duplicate_rows / len(self.df) * 100)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Quality metrics table
        quality_data = [
            ['Metric', 'Value'],
            ['Total Records', f"{len(self.df):,}"],
            ['Total Columns', f"{len(self.df.columns):,}"],
            ['Total Cells', f"{total_cells:,}"],
            ['Missing Cells', f"{missing_cells:,}"],
            ['Completeness %', f"{completeness:.2f}%"],
            ['Duplicate Rows', f"{duplicate_rows:,}"],
            ['Duplicate %', f"{duplicate_pct:.2f}%"],
            ['Numeric Columns', f"{len(numeric_cols)}"],
            ['Categorical Columns', f"{len(self.df.select_dtypes(include=['object']).columns)}"],
        ]
        
        table = Table(quality_data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Quality visualization
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Completeness gauge
        completeness_data = [completeness, 100 - completeness]
        axes[0, 0].pie(completeness_data, labels=['Complete', 'Missing'], autopct='%1.1f%%', 
                       colors=['green', 'red'], startangle=90)
        axes[0, 0].set_title('Data Completeness', fontweight='bold', fontsize=12)
        
        # Missing data by column
        missing_by_col = self.df.isnull().sum()
        missing_by_col = missing_by_col[missing_by_col > 0].sort_values(ascending=False).head(10)
        if len(missing_by_col) > 0:
            missing_by_col.plot(kind='barh', ax=axes[0, 1], color='coral')
            axes[0, 1].set_title('Top 10 Columns with Missing Data', fontweight='bold', fontsize=12)
            axes[0, 1].set_xlabel('Count')
        
        # Data type distribution
        dtype_dist = self.df.dtypes.value_counts()
        axes[1, 0].bar(range(len(dtype_dist)), dtype_dist.values, color='steelblue')
        axes[1, 0].set_xticks(range(len(dtype_dist)))
        axes[1, 0].set_xticklabels([str(d) for d in dtype_dist.index], rotation=45, ha='right')
        axes[1, 0].set_title('Data Type Distribution', fontweight='bold', fontsize=12)
        axes[1, 0].set_ylabel('Count')
        
        # Duplicates pie
        duplicate_data = [len(self.df) - duplicate_rows, duplicate_rows]
        axes[1, 1].pie(duplicate_data, labels=['Unique', 'Duplicates'], autopct='%1.1f%%',
                       colors=['green', 'orange'], startangle=90)
        axes[1, 1].set_title('Record Uniqueness', fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        img = Image(self._img_to_bytes(fig), width=5.5*inch, height=5*inch)
        self.story.append(img)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_advanced_statistics(self):
        """Add advanced statistical analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("17. ADVANCED STATISTICS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Create advanced stats table
        stats_data = [['Column', 'Mean', 'Median', 'Std Dev', 'Skewness', 'Kurtosis', 'CV%']]
        
        for col in numeric_cols[:10]:  # Limit to first 10
            try:
                mean = self.df[col].mean()
                median = self.df[col].median()
                std = self.df[col].std()
                skewness = self.df[col].skew()
                kurtosis = self.df[col].kurtosis()
                cv = (std / mean * 100) if mean != 0 else 0
                
                stats_data.append([
                    col[:15],
                    f"{mean:.2f}",
                    f"{median:.2f}",
                    f"{std:.2f}",
                    f"{skewness:.2f}",
                    f"{kurtosis:.2f}",
                    f"{cv:.2f}%"
                ])
            except:
                pass
        
        table = Table(stats_data, colWidths=[1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.7*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_missing_data_imputation_hints(self):
        """Add imputation recommendations for missing data"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("18. MISSING DATA IMPUTATION RECOMMENDATIONS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        missing_data = self.df.isnull().sum()
        missing_cols = missing_data[missing_data > 0]
        
        if len(missing_cols) > 0:
            recommendations = [['Column', 'Missing Count', 'Missing %', 'Recommended Strategy']]
            
            for col in missing_cols.index:
                missing_pct = (missing_cols[col] / len(self.df)) * 100
                
                # Recommendation logic
                if missing_pct > 50:
                    strategy = 'Consider removing column (>50% missing)'
                elif missing_pct > 20:
                    strategy = 'Multiple imputation or domain knowledge'
                else:
                    col_dtype = self.df[col].dtype
                    if col_dtype in ['int64', 'float64']:
                        strategy = 'Mean/Median imputation or KNN'
                    else:
                        strategy = 'Mode imputation or forward fill'
                
                recommendations.append([
                    col[:20],
                    str(int(missing_cols[col])),
                    f"{missing_pct:.2f}%",
                    strategy
                ])
            
            table = Table(recommendations, colWidths=[1.5*inch, 1.2*inch, 1*inch, 2.3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            self.story.append(table)
        else:
            self.story.append(Paragraph("✅ No missing data to impute", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_feature_importance_analysis(self):
        """Add feature importance analysis using Random Forest"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("19. FEATURE IMPORTANCE ANALYSIS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        try:
            numeric_df = self.df.select_dtypes(include=[np.number])
            
            if numeric_df.shape[1] > 1:
                # Use first numeric column as target for demonstration
                target_col = numeric_df.columns[0]
                features = numeric_df.drop(columns=[target_col])
                
                if features.shape[1] > 0:
                    # Remove rows with missing values
                    clean_df = numeric_df.dropna()
                    
                    if len(clean_df) > 0:
                        X = clean_df[features.columns]
                        y = clean_df[target_col]
                        
                        # Train Random Forest
                        model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)
                        model.fit(X, y)
                        
                        # Get feature importance
                        importances = model.feature_importances_
                        feature_importance_df = pd.DataFrame({
                            'Feature': features.columns,
                            'Importance': importances
                        }).sort_values('Importance', ascending=False)
                        
                        # Plot
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.barh(range(len(feature_importance_df)), feature_importance_df['Importance'], color='steelblue')
                        ax.set_yticks(range(len(feature_importance_df)))
                        ax.set_yticklabels(feature_importance_df['Feature'])
                        ax.set_xlabel('Importance Score')
                        ax.set_title(f'Feature Importance (Target: {target_col})', fontweight='bold', fontsize=12)
                        ax.invert_yaxis()
                        ax.grid(alpha=0.3, axis='x')
                        
                        plt.tight_layout()
                        img = Image(self._img_to_bytes(fig), width=5.5*inch, height=4*inch)
                        self.story.append(img)
                        self.story.append(Spacer(1, 0.2*inch))
            
            self.story.append(Paragraph("Note: Feature importance based on Random Forest model", self.styles['Normal']))
        except:
            self.story.append(Paragraph("Could not compute feature importance", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_insights_summary(self):
        """Add comprehensive insights summary"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("20. KEY INSIGHTS & RECOMMENDATIONS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        insights = []
        
        # Data quality insights
        completeness = ((self.df.shape[0] * self.df.shape[1] - self.df.isnull().sum().sum()) / (self.df.shape[0] * self.df.shape[1]) * 100)
        if completeness < 95:
            insights.append(f"⚠️ Data Completeness: {completeness:.1f}% - Missing data detected, consider imputation strategies")
        else:
            insights.append(f"✅ Data Completeness: {completeness:.1f}% - Excellent data quality")
        
        # Duplicate insights
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            insights.append(f"⚠️ Duplicates Found: {duplicates} duplicate rows detected - Consider deduplication")
        else:
            insights.append(f"✅ No Duplicates: All records are unique")
        
        # Distribution insights
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        skewed_cols = []
        for col in numeric_cols:
            if abs(self.df[col].skew()) > 1:
                skewed_cols.append(col)
        
        if skewed_cols:
            insights.append(f"📊 Skewed Distributions: {', '.join(skewed_cols[:3])} - Consider transformation for ML")
        
        # Correlation insights
        if len(numeric_cols) > 1:
            corr_matrix = self.df[numeric_cols].corr()
            strong_corr_count = ((corr_matrix.abs() > 0.7).sum().sum() - len(numeric_cols)) // 2
            if strong_corr_count > 0:
                insights.append(f"🔗 Multicollinearity: {strong_corr_count} strong correlations detected - May need feature selection")
        
        # Categorical insights
        cat_cols = self.df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            insights.append(f"📁 Categorical Features: {len(cat_cols)} categorical columns - Encoding required for ML models")
        
        # Data type insights
        insights.append(f"📝 Data Types: {len(numeric_cols)} numeric, {len(cat_cols)} categorical columns")
        
        # Recommendations
        recommendations = [
            "1. Data Preprocessing: Handle missing values and outliers before modeling",
            "2. Feature Engineering: Create meaningful features from existing data",
            "3. Scaling: Normalize/standardize numeric features for ML algorithms",
            "4. Encoding: Apply appropriate encoding for categorical variables",
            "5. Validation: Use train-test split and cross-validation for model evaluation",
            "6. Monitoring: Track data quality metrics over time"
        ]
        
        self.story.append(Paragraph("<b>📈 Key Insights:</b>", self.styles['Normal']))
        for insight in insights:
            self.story.append(Paragraph(f"• {insight}", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.2*inch))
        self.story.append(Paragraph("<b>💡 Recommendations:</b>", self.styles['Normal']))
        for rec in recommendations:
            self.story.append(Paragraph(rec, self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def generate_report(self):
        """Generate full EDA PDF report with ALL visualizations, dashboards and insights"""
        self._create_title_page()
        self._add_missing_data_visualization()
        self._add_distribution_charts()
        self._add_box_plots()
        self._add_correlation_heatmap()
        self._add_categorical_charts()
        self._add_pairplot()
        self._add_distribution_comparison()
        self._add_statistical_summary_charts()
        self._add_data_type_summary()
        self._add_summary_statistics()
        self._add_outlier_analysis()
        self._add_feature_correlation_insights()
        self._add_normality_tests()
        self._add_feature_distribution_matrix()
        self._add_categorical_insights()
        self._add_data_quality_dashboard()
        self._add_advanced_statistics()
        self._add_missing_data_imputation_hints()
        self._add_feature_importance_analysis()
        self._add_insights_summary()
        
        # Create PDF
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        doc.build(self.story)
        self.buffer.seek(0)
        
        return self.buffer.getvalue()
