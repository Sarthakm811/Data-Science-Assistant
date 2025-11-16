"""
Automated EDA Tool - Comprehensive exploratory data analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List
from pathlib import Path


class EDAToolError(Exception):
    pass


class EDATool:
    """Automated Exploratory Data Analysis"""

    def __init__(self, output_dir: str = "/outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_style("whitegrid")

    def perform_full_eda(self, df: pd.DataFrame, job_id: str) -> Dict[str, Any]:
        """
        Comprehensive EDA pipeline
        Returns insights and saves visualizations
        """
        results = {
            "basic_info": self._get_basic_info(df),
            "summary_stats": self._get_summary_stats(df),
            "missing_data": self._analyze_missing_data(df),
            "correlations": self._analyze_correlations(df),
            "distributions": self._analyze_distributions(df, job_id),
            "outliers": self._detect_outliers(df),
            "categorical_analysis": self._analyze_categorical(df, job_id),
            "visualizations": [],
        }

        # Generate visualizations
        viz_paths = self._generate_visualizations(df, job_id)
        results["visualizations"] = viz_paths

        return results

    def _get_basic_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Basic dataset information"""
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2,
        }

    def _get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Summary statistics for numeric columns"""
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return {}

        stats = numeric_df.describe().to_dict()

        # Add additional stats
        for col in numeric_df.columns:
            stats[col]["skewness"] = float(numeric_df[col].skew())
            stats[col]["kurtosis"] = float(numeric_df[col].kurtosis())

        return stats

    def _analyze_missing_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing data patterns"""
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100

        return {
            "total_missing": int(missing.sum()),
            "columns_with_missing": {
                col: {"count": int(missing[col]), "percentage": float(missing_pct[col])}
                for col in missing[missing > 0].index
            },
        }

    def _analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Correlation analysis for numeric features"""
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] < 2:
            return {}

        corr_matrix = numeric_df.corr()

        # Find high correlations
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > 0.7:
                    high_corr.append(
                        {
                            "feature1": corr_matrix.columns[i],
                            "feature2": corr_matrix.columns[j],
                            "correlation": float(corr_matrix.iloc[i, j]),
                        }
                    )

        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "high_correlations": high_corr,
        }

    def _analyze_distributions(self, df: pd.DataFrame, job_id: str) -> Dict[str, Any]:
        """Analyze distributions of numeric features"""
        numeric_df = df.select_dtypes(include=[np.number])
        distributions = {}

        for col in numeric_df.columns:
            distributions[col] = {
                "mean": float(numeric_df[col].mean()),
                "median": float(numeric_df[col].median()),
                "std": float(numeric_df[col].std()),
                "min": float(numeric_df[col].min()),
                "max": float(numeric_df[col].max()),
                "unique_values": int(numeric_df[col].nunique()),
            }

        return distributions

    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers using IQR method"""
        numeric_df = df.select_dtypes(include=[np.number])
        outliers = {}

        for col in numeric_df.columns:
            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outlier_count = (
                (numeric_df[col] < lower_bound) | (numeric_df[col] > upper_bound)
            ).sum()

            if outlier_count > 0:
                outliers[col] = {
                    "count": int(outlier_count),
                    "percentage": float((outlier_count / len(df)) * 100),
                    "lower_bound": float(lower_bound),
                    "upper_bound": float(upper_bound),
                }

        return outliers

    def _analyze_categorical(self, df: pd.DataFrame, job_id: str) -> Dict[str, Any]:
        """Analyze categorical features"""
        categorical_df = df.select_dtypes(include=["object", "category"])
        analysis = {}

        for col in categorical_df.columns:
            value_counts = df[col].value_counts()
            analysis[col] = {
                "unique_values": int(df[col].nunique()),
                "most_common": value_counts.head(10).to_dict(),
                "missing": int(df[col].isnull().sum()),
            }

        return analysis

    def _generate_visualizations(self, df: pd.DataFrame, job_id: str) -> List[str]:
        """Generate comprehensive visualizations"""
        viz_paths = []

        # 1. Correlation heatmap
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] >= 2:
            plt.figure(figsize=(12, 10))
            sns.heatmap(
                numeric_df.corr(), annot=True, cmap="coolwarm", center=0, fmt=".2f"
            )
            plt.title("Correlation Heatmap")
            path = self.output_dir / f"{job_id}_correlation_heatmap.png"
            plt.savefig(path, dpi=300, bbox_inches="tight")
            plt.close()
            viz_paths.append(str(path))

        # 2. Distribution plots for numeric features
        if not numeric_df.empty:
            n_cols = min(4, len(numeric_df.columns))
            n_rows = (len(numeric_df.columns) + n_cols - 1) // n_cols
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5 * n_rows))
            axes = axes.flatten() if n_rows > 1 else [axes]

            for idx, col in enumerate(numeric_df.columns):
                if idx < len(axes):
                    numeric_df[col].hist(bins=30, ax=axes[idx], edgecolor="black")
                    axes[idx].set_title(f"Distribution of {col}")
                    axes[idx].set_xlabel(col)
                    axes[idx].set_ylabel("Frequency")

            # Hide empty subplots
            for idx in range(len(numeric_df.columns), len(axes)):
                axes[idx].axis("off")

            plt.tight_layout()
            path = self.output_dir / f"{job_id}_distributions.png"
            plt.savefig(path, dpi=300, bbox_inches="tight")
            plt.close()
            viz_paths.append(str(path))

        # 3. Box plots for outlier detection
        if not numeric_df.empty and len(numeric_df.columns) <= 10:
            plt.figure(figsize=(15, 6))
            numeric_df.boxplot()
            plt.title("Box Plots - Outlier Detection")
            plt.xticks(rotation=45, ha="right")
            path = self.output_dir / f"{job_id}_boxplots.png"
            plt.savefig(path, dpi=300, bbox_inches="tight")
            plt.close()
            viz_paths.append(str(path))

        # 4. Missing data visualization
        if df.isnull().sum().sum() > 0:
            plt.figure(figsize=(12, 6))
            missing_data = df.isnull().sum()
            missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
            missing_data.plot(kind="bar")
            plt.title("Missing Data by Column")
            plt.xlabel("Columns")
            plt.ylabel("Number of Missing Values")
            plt.xticks(rotation=45, ha="right")
            path = self.output_dir / f"{job_id}_missing_data.png"
            plt.savefig(path, dpi=300, bbox_inches="tight")
            plt.close()
            viz_paths.append(str(path))

        # 5. Pairplot for top numeric features (if not too many)
        if 2 <= numeric_df.shape[1] <= 5 and len(df) <= 1000:
            try:
                pairplot = sns.pairplot(numeric_df.sample(min(500, len(df))))
                path = self.output_dir / f"{job_id}_pairplot.png"
                pairplot.savefig(path, dpi=300, bbox_inches="tight")
                plt.close()
                viz_paths.append(str(path))
            except Exception as e:
                print(f"Pairplot generation failed: {e}")

        return viz_paths

    def generate_eda_summary(self, results: Dict[str, Any]) -> str:
        """Generate human-readable EDA summary"""
        summary = []

        # Basic info
        info = results["basic_info"]
        summary.append("📊 Dataset Overview:")
        summary.append(
            f"  - Shape: {info['shape'][0]} rows × {info['shape'][1]} columns"
        )
        summary.append(f"  - Memory: {info['memory_usage_mb']:.2f} MB")

        # Missing data
        missing = results["missing_data"]
        if missing["total_missing"] > 0:
            summary.append("\n⚠️ Missing Data:")
            summary.append(f"  - Total missing values: {missing['total_missing']}")
            for col, data in list(missing["columns_with_missing"].items())[:5]:
                summary.append(
                    f"  - {col}: {data['count']} ({data['percentage']:.1f}%)"
                )

        # Correlations
        corr = results.get("correlations", {})
        if corr.get("high_correlations"):
            summary.append("\n🔗 High Correlations:")
            for item in corr["high_correlations"][:5]:
                summary.append(
                    f"  - {item['feature1']} ↔ {item['feature2']}: {item['correlation']:.2f}"
                )

        # Outliers
        outliers = results.get("outliers", {})
        if outliers:
            summary.append("\n📍 Outliers Detected:")
            for col, data in list(outliers.items())[:5]:
                summary.append(
                    f"  - {col}: {data['count']} outliers ({data['percentage']:.1f}%)"
                )

        return "\n".join(summary)
