"""Advanced Data Processing Module"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    def __init__(self, df):
        self.df = df.copy()
        self.original_df = df.copy()
    
    def missing_value_analysis(self):
        """Analyze missing values"""
        missing = self.df.isnull().sum()
        missing_percent = (missing / len(self.df) * 100).round(2)
        
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Count': missing.values,
            'Missing %': missing_percent.values
        }).sort_values('Missing %', ascending=False)
        
        return missing_df[missing_df['Missing Count'] > 0]
    
    def impute_missing(self, strategy='mean', columns=None):
        """Impute missing values"""
        if columns is None:
            columns = self.df.columns
        
        if strategy == 'mean':
            imputer = SimpleImputer(strategy='mean')
        elif strategy == 'median':
            imputer = SimpleImputer(strategy='median')
        elif strategy == 'mode':
            imputer = SimpleImputer(strategy='most_frequent')
        elif strategy == 'knn':
            imputer = KNNImputer(n_neighbors=5)
        
        self.df[columns] = imputer.fit_transform(self.df[columns])
        return self.df
    
    def handle_duplicates(self, subset=None, keep='first'):
        """Handle duplicate rows"""
        duplicates = self.df.duplicated(subset=subset, keep=False).sum()
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        return self.df, duplicates
    
    def encode_categorical(self, columns, method='label'):
        """Encode categorical variables"""
        for col in columns:
            if method == 'label':
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col].astype(str))
            elif method == 'onehot':
                dummies = pd.get_dummies(self.df[col], prefix=col)
                self.df = pd.concat([self.df, dummies], axis=1)
                self.df = self.df.drop(col, axis=1)
        
        return self.df
    
    def scale_features(self, columns, method='standard'):
        """Scale numeric features"""
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        
        self.df[columns] = scaler.fit_transform(self.df[columns])
        return self.df
    
    def handle_outliers(self, columns, method='iqr', threshold=1.5):
        """Handle outliers"""
        outlier_count = 0
        
        for col in columns:
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - threshold * IQR
                upper = Q3 + threshold * IQR
                
                outliers = (self.df[col] < lower) | (self.df[col] > upper)
                outlier_count += outliers.sum()
                
                self.df.loc[outliers, col] = self.df[col].median()
            
            elif method == 'zscore':
                from scipy import stats
                z_scores = np.abs(stats.zscore(self.df[col].dropna()))
                outliers = z_scores > threshold
                outlier_count += outliers.sum()
                
                self.df.loc[self.df[col].index[outliers], col] = self.df[col].median()
        
        return self.df, outlier_count
    
    def balance_dataset(self, target_col, method='smote'):
        """Balance imbalanced dataset"""
        X = self.df.drop(target_col, axis=1)
        y = self.df[target_col]
        
        # Check if target is categorical (for classification)
        if y.dtype == 'object' or len(y.unique()) < 20:
            # Classification task
            if method == 'smote':
                try:
                    smote = SMOTE(random_state=42)
                    X_balanced, y_balanced = smote.fit_resample(X, y)
                except Exception as e:
                    return self.df, f"SMOTE failed: {str(e)}"
            elif method == 'undersample':
                rus = RandomUnderSampler(random_state=42)
                X_balanced, y_balanced = rus.fit_resample(X, y)
            
            balanced_df = pd.concat([X_balanced, y_balanced], axis=1)
            return balanced_df
        else:
            # Regression task - cannot use SMOTE
            return self.df, "Target appears to be continuous (regression). Balancing only works for classification tasks."
    
    def merge_datasets(self, other_df, on, how='inner'):
        """Merge datasets"""
        merged = pd.merge(self.df, other_df, on=on, how=how)
        return merged
    
    def get_data_quality_score(self):
        """Calculate data quality score"""
        score = 100
        
        # Missing values
        missing_percent = self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)) * 100
        score -= missing_percent * 0.5
        
        # Duplicates
        duplicate_percent = self.df.duplicated().sum() / len(self.df) * 100
        score -= duplicate_percent * 0.3
        
        return max(0, score)
