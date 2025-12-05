"""
Advanced EDA Engine
Statistical analysis, tests, and data quality assessment
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from scipy import stats
from scipy.stats import (
    shapiro, normaltest, anderson, jarque_bera,
    chi2_contingency, pearsonr, spearmanr, kendalltau,
    ttest_ind, mannwhitneyu, kruskal, f_oneway
)
import warnings

warnings.filterwarnings('ignore')


class EDAEngine:
    """Comprehensive Exploratory Data Analysis Engine"""
    
    def __init__(self):
        pass
    
    def full_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Run complete EDA analysis"""
        
        results = {
            "summary": self._get_summary(df),
            "data_types": self._analyze_data_types(df),
            "missing_data": self._analyze_missing(df),
            "statistics": self._get_statistics(df),
            "distributions": self._analyze_distributions(df),
            "correlations": self._analyze_correlations(df),
            "categorical_analysis": self._analyze_categorical(df),
            "outliers": self._detect_outliers(df),
            "data_quality": self._assess_data_quality(df),
            "normality_tests": self._test_normality(df),
            "recommendations": self._generate_recommendations(df)
        }
        
        return results
    
    def _get_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get dataset summary"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_columns": len(numeric_cols),
            "categorical_columns": len(categorical_cols),
            "datetime_columns": len(datetime_cols),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
            "duplicates": int(df.duplicated().sum()),
            "missing_cells": int(df.isnull().sum().sum()),
            "missing_percentage": round(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100, 2)
        }
    
    def _analyze_data_types(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analyze data types for each column"""
        results = []
        
        for col in df.columns:
            col_info = {
                "name": col,
                "dtype": str(df[col].dtype),
                "unique_values": int(df[col].nunique()),
                "unique_percentage": round(df[col].nunique() / len(df) * 100, 2),
                "missing": int(df[col].isnull().sum()),
                "missing_percentage": round(df[col].isnull().sum() / len(df) * 100, 2)
            }
            
            # Infer semantic type
            if df[col].dtype in ['int64', 'float64']:
                if df[col].nunique() <= 10:
                    col_info["semantic_type"] = "categorical_numeric"
                elif df[col].nunique() == len(df):
                    col_info["semantic_type"] = "identifier"
                else:
                    col_info["semantic_type"] = "continuous"
            elif df[col].dtype