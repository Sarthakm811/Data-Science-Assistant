"""Comprehensive PDF Report Generator with Full EDA"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class ComprehensivePDFReport:
    def __init__(self, df, dataset_name="Dataset"):
        self.df = df
        self.dataset_name = dataset_name
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.buffer = io.BytesIO()
        self.story = []
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles"""
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
    
    def _create_title_page(self):
        """Create title page"""
        self.story.append(Spacer(1, 2*inch))
        
        title = Paragraph(
            "📊 Comprehensive Data Analysis Report",
            self.styles['CustomTitle']
        )
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
    
    def _add_table_of_contents(self):
        """Add table of contents"""
        toc_title = Paragraph("📑 Table of Contents", self.styles['CustomHeading'])
        self.story.append(toc_title)
        self.story.append(Spacer(1, 0.2*inch))
        
        toc_items = [
            "1. Dataset Overview",
            "2. Data Quality Assessment",
            "3. Missing Values Analysis",
            "4. Descriptive Statistics",
            "5. Data Types & Distributions",
            "6. Correlation Analysis",
            "7. Statistical Tests",
            "8. Outlier Detection",
            "9. Data Recommendations"
        ]
        
        for item in toc_items:
            self.story.append(Paragraph(item, self.styles['Normal']))
            self.story.append(Spacer(1, 0.1*inch))
        
        self.story.append(PageBreak())
    
    def _add_dataset_overview(self):
        """Add dataset overview section"""
        self.story.append(Paragraph("1. Dataset Overview", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        overview_data = [
            ['Metric', 'Value'],
            ['Total Rows', str(self.df.shape[0])],
            ['Total Columns', str(self.df.shape[1])],
            ['Memory Usage', f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"],
            ['Duplicate Rows', str(self.df.duplicated().sum())],
            ['Complete Rows', str(len(self.df.dropna()))],
            ['Completeness %', f"{(1 - self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100:.2f}%"]
        ]
        
        table = Table(overview_data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_data_quality(self):
        """Add data quality assessment"""
        self.story.append(Paragraph("2. Data Quality Assessment", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Calculate quality score
        missing_percent = self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)) * 100
        duplicate_percent = self.df.duplicated().sum() / len(self.df) * 100
        quality_score = max(0, 100 - missing_percent * 0.5 - duplicate_percent * 0.3)
        
        quality_text = f"""
        <b>Data Quality Score: {quality_score:.2f}/100</b><br/>
        <br/>
        <b>Quality Factors:</b><br/>
        • Missing Data Impact: {missing_percent:.2f}%<br/>
        • Duplicate Rows Impact: {duplicate_percent:.2f}%<br/>
        • Overall Completeness: {100 - missing_percent:.2f}%<br/>
        <br/>
        <b>Assessment:</b><br/>
        """
        
        if quality_score >= 90:
            quality_text += "✅ Excellent data quality - Ready for analysis"
        elif quality_score >= 75:
            quality_text += "⚠️ Good data quality - Minor cleaning recommended"
        elif quality_score >= 50:
            quality_text += "⚠️ Fair data quality - Significant cleaning needed"
        else:
            quality_text += "❌ Poor data quality - Extensive cleaning required"
        
        self.story.append(Paragraph(quality_text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_missing_values(self):
        """Add missing values analysis"""
        self.story.append(Paragraph("3. Missing Values Analysis", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df) * 100).round(2)
        
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Count': missing.values,
            'Missing %': missing_percent.values
        }).sort_values('Missing %', ascending=False)
        
        missing_df = missing_df[missing_df['Missing Count'] > 0]
        
        if len(missing_df) > 0:
            data = [['Column', 'Missing Count', 'Missing %']]
            for _, row in missing_df.iterrows():
                data.append([str(row['Column']), str(row['Missing Count']), f"{row['Missing %']:.2f}%"])
            
            table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            self.story.append(table)
        else:
            self.story.append(Paragraph("✅ No missing values found!", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_descriptive_stats(self):
        """Add descriptive statistics"""
        self.story.append(Paragraph("4. Descriptive Statistics", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        stats_summary = numeric_df.describe().round(4)
        
        data = [['Statistic'] + list(stats_summary.columns)]
        for idx, row in stats_summary.iterrows():
            data.append([str(idx)] + [f"{val:.4f}" if isinstance(val, float) else str(val) for val in row])
        
        table = Table(data, colWidths=[1.2*inch] + [0.8*inch] * len(stats_summary.columns))
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
    
    def _add_data_types(self):
        """Add data types information"""
        self.story.append(Paragraph("5. Data Types & Distributions", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        dtype_counts = self.df.dtypes.value_counts()
        
        data = [['Data Type', 'Count']]
        for dtype, count in dtype_counts.items():
            data.append([str(dtype), str(count)])
        
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_correlation_analysis(self):
        """Add correlation analysis"""
        self.story.append(Paragraph("6. Correlation Analysis", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            
            # Create correlation heatmap
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
            ax.set_title('Correlation Heatmap')
            
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close(fig)
            
            img = Image(img_buffer, width=5*inch, height=4*inch)
            self.story.append(img)
            
            # Top correlations
            self.story.append(Spacer(1, 0.2*inch))
            self.story.append(Paragraph("<b>Top Correlations:</b>", self.styles['Normal']))
            
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_pairs.append({
                        'Var1': corr_matrix.columns[i],
                        'Var2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
            
            corr_pairs_df = pd.DataFrame(corr_pairs).sort_values('Correlation', key=abs, ascending=False).head(5)
            
            for _, row in corr_pairs_df.iterrows():
                self.story.append(Paragraph(
                    f"• {row['Var1']} ↔ {row['Var2']}: {row['Correlation']:.4f}",
                    self.styles['Normal']
                ))
        else:
            self.story.append(Paragraph("Not enough numeric columns for correlation analysis", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_statistical_tests(self):
        """Add statistical tests"""
        self.story.append(Paragraph("7. Statistical Tests", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        from scipy import stats
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        test_results = []
        for col in numeric_cols[:5]:  # Limit to first 5 columns
            data = self.df[col].dropna()
            if len(data) > 3:
                shapiro_stat, shapiro_p = stats.shapiro(data)
                test_results.append({
                    'Column': col,
                    'Shapiro-Wilk p-value': f"{shapiro_p:.4f}",
                    'Normal': "Yes" if shapiro_p > 0.05 else "No"
                })
        
        if test_results:
            data = [['Column', 'Shapiro-Wilk p-value', 'Normal Distribution']]
            for result in test_results:
                data.append([result['Column'], result['Shapiro-Wilk p-value'], result['Normal']])
            
            table = Table(data, colWidths=[2*inch, 2*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            self.story.append(table)
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_outlier_detection(self):
        """Add outlier detection"""
        self.story.append(Paragraph("8. Outlier Detection", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        outlier_summary = []
        for col in numeric_df.columns[:5]:  # Limit to first 5 columns
            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            outliers = ((numeric_df[col] < lower) | (numeric_df[col] > upper)).sum()
            outlier_summary.append({
                'Column': col,
                'Outliers': outliers,
                'Percentage': f"{(outliers / len(numeric_df) * 100):.2f}%"
            })
        
        data = [['Column', 'Outlier Count', 'Percentage']]
        for item in outlier_summary:
            data.append([item['Column'], str(item['Outliers']), item['Percentage']])
        
        table = Table(data, colWidths=[2*inch, 2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_recommendations(self):
        """Add data recommendations"""
        self.story.append(Paragraph("9. Data Recommendations", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        recommendations = []
        
        # Check for missing values
        if self.df.isnull().sum().sum() > 0:
            recommendations.append("• Handle missing values using imputation techniques")
        
        # Check for duplicates
        if self.df.duplicated().sum() > 0:
            recommendations.append("• Remove duplicate rows to avoid bias")
        
        # Check for outliers
        numeric_df = self.df.select_dtypes(include=[np.number])
        if len(numeric_df) > 0:
            for col in numeric_df.columns[:3]:
                Q1 = numeric_df[col].quantile(0.25)
                Q3 = numeric_df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((numeric_df[col] < Q1 - 1.5*IQR) | (numeric_df[col] > Q3 + 1.5*IQR)).sum()
                if outliers > 0:
                    recommendations.append(f"• Investigate and handle outliers in '{col}'")
                    break
        
        # Check for categorical encoding
        cat_cols = self.df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            recommendations.append("• Encode categorical variables for machine learning")
        
        # Check for scaling
        if len(numeric_df) > 0:
            recommendations.append("• Consider feature scaling for better model performance")
        
        if not recommendations:
            recommendations.append("✅ Dataset appears to be well-prepared for analysis")
        
        for rec in recommendations:
            self.story.append(Paragraph(rec, self.styles['Normal']))
            self.story.append(Spacer(1, 0.1*inch))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_distribution_visualizations(self):
        """Add distribution plots for numeric columns"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("10. Distribution Analysis", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:4]:  # Limit to first 4 columns
            try:
                fig, ax = plt.subplots(figsize=(6, 4))
                self.df[col].hist(bins=30, ax=ax, edgecolor='black', alpha=0.7)
                ax.set_title(f'Distribution: {col}')
                ax.set_xlabel(col)
                ax.set_ylabel('Frequency')
                
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close(fig)
                
                img = Image(img_buffer, width=3.5*inch, height=2.5*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 0.2*inch))
            except:
                pass
    
    def _add_box_plots(self):
        """Add box plots for outlier visualization"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("11. Box Plot Analysis (Outlier Detection)", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(10, 8))
            axes = axes.flatten()
            
            for idx, col in enumerate(numeric_cols[:4]):
                axes[idx].boxplot(self.df[col].dropna())
                axes[idx].set_title(f'Box Plot: {col}')
                axes[idx].set_ylabel(col)
            
            plt.tight_layout()
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close(fig)
            
            img = Image(img_buffer, width=5*inch, height=4*inch)
            self.story.append(img)
        except:
            pass
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_pairplot_analysis(self):
        """Add pairplot for relationship analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("12. Relationship Analysis (Pairplot)", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 2:
            try:
                # Create a subset for pairplot (limit to 4 columns to avoid too large plot)
                subset_cols = numeric_cols[:4]
                fig = sns.pairplot(self.df[subset_cols], diag_kind='hist', plot_kws={'alpha': 0.6})
                
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close(fig)
                
                img = Image(img_buffer, width=5.5*inch, height=5.5*inch)
                self.story.append(img)
            except:
                self.story.append(Paragraph("Pairplot could not be generated", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_skewness_kurtosis(self):
        """Add skewness and kurtosis analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("13. Skewness & Kurtosis Analysis", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        skew_kurt_data = []
        for col in numeric_cols[:8]:  # Limit to first 8 columns
            skewness = self.df[col].skew()
            kurtosis = self.df[col].kurtosis()
            skew_kurt_data.append([col, f"{skewness:.4f}", f"{kurtosis:.4f}"])
        
        if skew_kurt_data:
            data = [['Column', 'Skewness', 'Kurtosis']] + skew_kurt_data
            table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            self.story.append(table)
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_categorical_analysis(self):
        """Add categorical variable analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("14. Categorical Variables Analysis", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        cat_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(cat_cols) > 0:
            for col in cat_cols[:3]:  # Limit to first 3 categorical columns
                try:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    value_counts = self.df[col].value_counts().head(10)
                    value_counts.plot(kind='bar', ax=ax, color='steelblue')
                    ax.set_title(f'Value Counts: {col}')
                    ax.set_xlabel(col)
                    ax.set_ylabel('Count')
                    plt.xticks(rotation=45, ha='right')
                    
                    img_buffer = io.BytesIO()
                    fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                    img_buffer.seek(0)
                    plt.close(fig)
                    
                    img = Image(img_buffer, width=4.5*inch, height=2.5*inch)
                    self.story.append(img)
                    self.story.append(Spacer(1, 0.2*inch))
                except:
                    pass
        else:
            self.story.append(Paragraph("No categorical variables found", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_summary_insights(self):
        """Add summary insights and key findings"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("15. Key Insights & Summary", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        insights = []
        
        # Dataset size insight
        insights.append(f"<b>Dataset Size:</b> {self.df.shape[0]} rows and {self.df.shape[1]} columns")
        
        # Missing data insight
        missing_pct = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        if missing_pct == 0:
            insights.append("<b>Data Completeness:</b> ✅ No missing values detected")
        else:
            insights.append(f"<b>Data Completeness:</b> ⚠️ {missing_pct:.2f}% missing data")
        
        # Numeric columns insight
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        insights.append(f"<b>Numeric Columns:</b> {len(numeric_cols)} columns")
        
        # Categorical columns insight
        cat_cols = self.df.select_dtypes(include=['object']).columns
        insights.append(f"<b>Categorical Columns:</b> {len(cat_cols)} columns")
        
        # Duplicates insight
        duplicates = self.df.duplicated().sum()
        if duplicates == 0:
            insights.append("<b>Duplicates:</b> ✅ No duplicate rows found")
        else:
            insights.append(f"<b>Duplicates:</b> ⚠️ {duplicates} duplicate rows detected")
        
        # Correlation insight
        if len(numeric_cols) > 1:
            corr_matrix = self.df[numeric_cols].corr()
            high_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.8:
                        high_corr.append(f"{corr_matrix.columns[i]} ↔ {corr_matrix.columns[j]}")
            
            if high_corr:
                insights.append(f"<b>High Correlations:</b> Found {len(high_corr)} highly correlated pairs")
        
        for insight in insights:
            self.story.append(Paragraph(insight, self.styles['Normal']))
            self.story.append(Spacer(1, 0.15*inch))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def generate_report(self):
        """Generate complete PDF report with all EDA visualizations"""
        self._create_title_page()
        self._add_table_of_contents()
        self._add_dataset_overview()
        self._add_data_quality()
        self._add_missing_values()
        self._add_descriptive_stats()
        self._add_data_types()
        self._add_correlation_analysis()
        self._add_statistical_tests()
        self._add_outlier_detection()
        self._add_distribution_visualizations()
        self._add_box_plots()
        self._add_pairplot_analysis()
        self._add_skewness_kurtosis()
        self._add_categorical_analysis()
        self._add_summary_insights()
        self._add_recommendations()
        
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
