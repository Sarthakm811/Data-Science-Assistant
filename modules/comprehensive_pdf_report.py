"""Ultra-Comprehensive PDF Report Generator with ALL EDA Insights"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class UltraComprehensivePDFReport:
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
        title = Paragraph("📊 ULTRA-COMPREHENSIVE DATA ANALYSIS REPORT", self.styles['CustomTitle'])
        self.story.append(title)
        self.story.append(Spacer(1, 0.3*inch))
        
        subtitle = Paragraph(
            f"<b>Dataset:</b> {self.dataset_name}<br/>"
            f"<b>Generated:</b> {self.timestamp}<br/>"
            f"<b>Rows:</b> {self.df.shape[0]} | <b>Columns:</b> {self.df.shape[1]}<br/>"
            f"<b>Memory:</b> {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
            self.styles['Normal']
        )
        self.story.append(subtitle)
        self.story.append(PageBreak())
    
    def _add_executive_summary(self):
        """Add executive summary with key metrics"""
        self.story.append(Paragraph("EXECUTIVE SUMMARY", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        # Calculate key metrics
        missing_pct = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        duplicate_pct = (self.df.duplicated().sum() / len(self.df)) * 100
        quality_score = max(0, 100 - missing_pct * 0.5 - duplicate_pct * 0.3)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        cat_cols = self.df.select_dtypes(include=['object']).columns
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Rows', str(self.df.shape[0])],
            ['Total Columns', str(self.df.shape[1])],
            ['Numeric Columns', str(len(numeric_cols))],
            ['Categorical Columns', str(len(cat_cols))],
            ['Data Quality Score', f"{quality_score:.2f}/100"],
            ['Missing Data %', f"{missing_pct:.2f}%"],
            ['Duplicate Rows %', f"{duplicate_pct:.2f}%"],
            ['Memory Usage', f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"],
            ['Complete Rows', str(len(self.df.dropna()))]
        ]
        
        table = Table(summary_data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_all_distributions(self):
        """Add distribution plots for ALL numeric columns"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("DISTRIBUTION ANALYSIS - ALL NUMERIC COLUMNS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            try:
                fig, axes = plt.subplots(1, 2, figsize=(10, 3))
                
                # Histogram
                axes[0].hist(self.df[col].dropna(), bins=30, edgecolor='black', alpha=0.7, color='steelblue')
                axes[0].set_title(f'Distribution: {col}')
                axes[0].set_xlabel(col)
                axes[0].set_ylabel('Frequency')
                
                # Box plot
                axes[1].boxplot(self.df[col].dropna())
                axes[1].set_title(f'Box Plot: {col}')
                axes[1].set_ylabel(col)
                
                plt.tight_layout()
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close(fig)
                
                img = Image(img_buffer, width=5*inch, height=2*inch)
                self.story.append(img)
                
                # Add statistics
                stats_text = f"<b>{col}:</b> Mean={self.df[col].mean():.4f}, Median={self.df[col].median():.4f}, Std={self.df[col].std():.4f}, Skew={self.df[col].skew():.4f}, Kurt={self.df[col].kurtosis():.4f}"
                self.story.append(Paragraph(stats_text, self.styles['Normal']))
                self.story.append(Spacer(1, 0.15*inch))
            except:
                pass
    
    def _add_correlation_details(self):
        """Add detailed correlation analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("CORRELATION ANALYSIS - DETAILED", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) > 1:
            # Correlation heatmap
            fig, ax = plt.subplots(figsize=(10, 8))
            corr_matrix = numeric_df.corr()
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, cbar_kws={'label': 'Correlation'})
            ax.set_title('Correlation Matrix - All Numeric Columns')
            
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close(fig)
            
            img = Image(img_buffer, width=5.5*inch, height=4.5*inch)
            self.story.append(img)
            self.story.append(Spacer(1, 0.2*inch))
            
            # Top correlations
            self.story.append(Paragraph("<b>Top 15 Correlations (Excluding Diagonal):</b>", self.styles['Normal']))
            
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_pairs.append({
                        'Var1': corr_matrix.columns[i],
                        'Var2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
            
            corr_pairs_df = pd.DataFrame(corr_pairs).sort_values('Correlation', key=abs, ascending=False).head(15)
            
            data = [['Variable 1', 'Variable 2', 'Correlation']]
            for _, row in corr_pairs_df.iterrows():
                data.append([str(row['Var1']), str(row['Var2']), f"{row['Correlation']:.4f}"])
            
            table = Table(data, colWidths=[2*inch, 2*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            self.story.append(table)
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_categorical_details(self):
        """Add detailed categorical analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("CATEGORICAL VARIABLES ANALYSIS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        cat_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(cat_cols) > 0:
            for col in cat_cols:
                try:
                    fig, ax = plt.subplots(figsize=(10, 4))
                    value_counts = self.df[col].value_counts().head(15)
                    value_counts.plot(kind='barh', ax=ax, color='steelblue')
                    ax.set_title(f'Value Counts: {col} (Top 15)')
                    ax.set_xlabel('Count')
                    
                    img_buffer = io.BytesIO()
                    fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                    img_buffer.seek(0)
                    plt.close(fig)
                    
                    img = Image(img_buffer, width=5*inch, height=2.5*inch)
                    self.story.append(img)
                    
                    # Statistics
                    unique_count = self.df[col].nunique()
                    missing_count = self.df[col].isnull().sum()
                    stats_text = f"<b>{col}:</b> Unique Values={unique_count}, Missing={missing_count}, Mode={self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'N/A'}"
                    self.story.append(Paragraph(stats_text, self.styles['Normal']))
                    self.story.append(Spacer(1, 0.2*inch))
                except:
                    pass
        else:
            self.story.append(Paragraph("No categorical variables found", self.styles['Normal']))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_statistical_insights(self):
        """Add detailed statistical insights"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("STATISTICAL INSIGHTS & TESTS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Normality tests
        self.story.append(Paragraph("<b>Normality Tests (Shapiro-Wilk):</b>", self.styles['Normal']))
        
        test_data = [['Column', 'Statistic', 'P-Value', 'Normal?']]
        for col in numeric_cols[:10]:
            data = self.df[col].dropna()
            if len(data) > 3:
                stat, pvalue = stats.shapiro(data)
                is_normal = "✓ Yes" if pvalue > 0.05 else "✗ No"
                test_data.append([col, f"{stat:.4f}", f"{pvalue:.4f}", is_normal])
        
        table = Table(test_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
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
        
        # Skewness and Kurtosis
        self.story.append(Paragraph("<b>Skewness & Kurtosis Analysis:</b>", self.styles['Normal']))
        
        skew_data = [['Column', 'Skewness', 'Kurtosis', 'Interpretation']]
        for col in numeric_cols[:10]:
            skew = self.df[col].skew()
            kurt = self.df[col].kurtosis()
            
            if abs(skew) < 0.5:
                skew_interp = "Fairly Symmetric"
            elif skew > 0:
                skew_interp = "Right Skewed"
            else:
                skew_interp = "Left Skewed"
            
            skew_data.append([col, f"{skew:.4f}", f"{kurt:.4f}", skew_interp])
        
        table = Table(skew_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        self.story.append(table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def _add_outlier_analysis(self):
        """Add detailed outlier analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("OUTLIER DETECTION & ANALYSIS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        outlier_data = [['Column', 'Outliers (IQR)', 'Percentage', 'Min', 'Max']]
        
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            outliers = ((self.df[col] < lower) | (self.df[col] > upper)).sum()
            outlier_pct = (outliers / len(self.df)) * 100
            
            outlier_data.append([
                col,
                str(outliers),
                f"{outlier_pct:.2f}%",
                f"{self.df[col].min():.2f}",
                f"{self.df[col].max():.2f}"
            ])
        
        table = Table(outlier_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
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
    
    def _add_missing_data_analysis(self):
        """Add detailed missing data analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("MISSING DATA ANALYSIS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)
        
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Count': missing.values,
            'Missing %': missing_pct.values
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
    
    def _add_recommendations(self):
        """Add comprehensive recommendations"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("RECOMMENDATIONS & ACTION ITEMS", self.styles['CustomHeading']))
        self.story.append(Spacer(1, 0.2*inch))
        
        recommendations = []
        
        # Check for missing values
        if self.df.isnull().sum().sum() > 0:
            recommendations.append("🔴 CRITICAL: Handle missing values using appropriate imputation techniques")
        
        # Check for duplicates
        if self.df.duplicated().sum() > 0:
            recommendations.append("🟠 HIGH: Remove duplicate rows to avoid bias in analysis")
        
        # Check for outliers
        numeric_df = self.df.select_dtypes(include=[np.number])
        outlier_count = 0
        for col in numeric_df.columns:
            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((numeric_df[col] < Q1 - 1.5*IQR) | (numeric_df[col] > Q3 + 1.5*IQR)).sum()
            outlier_count += outliers
        
        if outlier_count > 0:
            recommendations.append(f"🟠 HIGH: Investigate and handle {outlier_count} outliers detected")
        
        # Check for categorical encoding
        cat_cols = self.df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            recommendations.append(f"🟡 MEDIUM: Encode {len(cat_cols)} categorical variables for ML models")
        
        # Check for scaling
        if len(numeric_df) > 0:
            recommendations.append("🟡 MEDIUM: Consider feature scaling (StandardScaler/MinMaxScaler) for better model performance")
        
        # Check for correlations
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            high_corr_count = 0
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.9:
                        high_corr_count += 1
            
            if high_corr_count > 0:
                recommendations.append(f"🟡 MEDIUM: {high_corr_count} highly correlated features detected - consider feature selection")
        
        if not recommendations:
            recommendations.append("✅ GREEN: Dataset appears well-prepared for analysis!")
        
        for rec in recommendations:
            self.story.append(Paragraph(rec, self.styles['Normal']))
            self.story.append(Spacer(1, 0.15*inch))
        
        self.story.append(Spacer(1, 0.3*inch))
    
    def generate_report(self):
        """Generate ultra-comprehensive PDF report"""
        self._create_title_page()
        self._add_executive_summary()
        self._add_all_distributions()
        self._add_correlation_details()
        self._add_categorical_details()
        self._add_statistical_insights()
        self._add_outlier_analysis()
        self._add_missing_data_analysis()
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
