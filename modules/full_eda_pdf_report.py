"""Full EDA PDF Report with ALL Charts and Graphs"""
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
from reportlab.lib.enums import TA_CENTER
from scipy import stats
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
                except:
                    pass
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
                fig = sns.pairplot(self.df[subset_cols], diag_kind='hist', plot_kws={'alpha': 0.6})
                
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close(fig)
                
                img = Image(img_buffer, width=5.5*inch, height=5.5*inch)
                self.story.append(img)
            except:
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
            except:
                pass
    
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
    
    def generate_report(self):
        """Generate full EDA PDF report"""
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
