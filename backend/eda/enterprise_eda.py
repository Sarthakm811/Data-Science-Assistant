"""
Enterprise EDA Orchestrator - Combines all analysis phases
"""

import pandas as pd
from typing import Dict, Optional
from .data_quality import DataQualityAnalyzer
from .structural_analysis import StructuralAnalyzer
from .statistical_analysis import StatisticalAnalyzer
from .correlation_analysis import CorrelationAnalyzer
from .ml_readiness import MLReadinessAnalyzer
from .advanced_viz import AdvancedVisualizer


class EnterpriseEDA:
    """
    Complete enterprise-grade EDA system
    Combines all analysis phases into one comprehensive report
    """

    def __init__(self, df: pd.DataFrame, target_col: Optional[str] = None):
        self.df = df
        self.target_col = target_col

        # Initialize all analyzers
        self.quality_analyzer = DataQualityAnalyzer(df)
        self.structural_analyzer = StructuralAnalyzer(df)
        self.statistical_analyzer = StatisticalAnalyzer(df)
        self.correlation_analyzer = CorrelationAnalyzer(df)
        self.ml_analyzer = MLReadinessAnalyzer(df, target_col)
        self.visualizer = AdvancedVisualizer(df)

    def run_complete_analysis(self) -> Dict:
        """
        Run all analysis phases and return comprehensive report
        """
        print("🔍 Running Enterprise EDA...")

        results = {
            "executive_summary": {},
            "phase1_data_quality": {},
            "phase2_structural": {},
            "phase3_statistical": {},
            "phase4_correlations": {},
            "phase5_ml_readiness": {},
            "recommendations": [],
        }

        # Phase 1: Data Quality (DRI)
        print("  Phase 1: Data Quality Assessment...")
        results["phase1_data_quality"] = self.quality_analyzer.calculate_dri()

        # Phase 2: Structural Analysis
        print("  Phase 2: Structural Analysis...")
        results["phase2_structural"] = self.structural_analyzer.get_schema_summary()

        # Phase 3: Statistical Analysis
        print("  Phase 3: Statistical Analysis...")
        results["phase3_statistical"] = (
            self.statistical_analyzer.get_comprehensive_report()
        )

        # Phase 4: Correlation Analysis
        print("  Phase 4: Correlation Analysis...")
        results["phase4_correlations"] = (
            self.correlation_analyzer.get_correlation_summary()
        )

        # Phase 5: ML Readiness
        print("  Phase 5: ML Readiness Assessment...")
        results["phase5_ml_readiness"] = self.ml_analyzer.assess_ml_readiness()

        # Generate Executive Summary
        results["executive_summary"] = self._generate_executive_summary(results)

        # Generate Recommendations
        results["recommendations"] = self._generate_recommendations(results)

        print("✅ Enterprise EDA Complete!")

        return results

    def _generate_executive_summary(self, results: Dict) -> Dict:
        """Generate executive summary from all phases"""
        dri = results["phase1_data_quality"]
        structural = results["phase2_structural"]
        statistical = results["phase3_statistical"]
        correlations = results["phase4_correlations"]
        ml_readiness = results["phase5_ml_readiness"]

        return {
            "dataset_shape": f"{len(self.df)} rows × {len(self.df.columns)} columns",
            "dri_score": dri.get("dri_score", 0),
            "dri_grade": dri.get("grade", "N/A"),
            "primary_keys": structural.get("primary_keys", []),
            "schema_quality": structural.get("schema_quality", {}).get(
                "quality_score", 0
            ),
            "non_normal_features": statistical.get("summary", {}).get(
                "non_normal_distributions", 0
            ),
            "high_correlations": correlations.get("pearson_high_count", 0),
            "multicollinearity_issues": correlations.get("multicollinearity_issues", 0),
            "ml_readiness_score": ml_readiness.get("overall_score", 0),
            "ml_readiness_grade": ml_readiness.get("readiness_grade", "N/A"),
            "critical_issues": dri.get("issues", []),
        }

    def _generate_recommendations(self, results: Dict) -> list:
        """Generate actionable recommendations"""
        recommendations = []

        # Data Quality Recommendations
        dri = results["phase1_data_quality"]
        if dri.get("dri_score", 0) < 80:
            recommendations.append(
                {
                    "category": "Data Quality",
                    "priority": "High",
                    "recommendation": "Improve data quality - DRI score below 80",
                    "actions": dri.get("issues", []),
                }
            )

        # Structural Recommendations
        structural = results["phase2_structural"]
        if not structural.get("primary_keys"):
            recommendations.append(
                {
                    "category": "Data Structure",
                    "priority": "Medium",
                    "recommendation": "No primary key detected",
                    "actions": ["Consider adding a unique identifier column"],
                }
            )

        # Statistical Recommendations
        statistical = results["phase3_statistical"]
        quality_flags = statistical.get("summary", {}).get("quality_flags", [])
        if any("⚠️" in flag for flag in quality_flags):
            recommendations.append(
                {
                    "category": "Statistical",
                    "priority": "Medium",
                    "recommendation": "Statistical issues detected",
                    "actions": quality_flags,
                }
            )

        # Correlation Recommendations
        correlations = results["phase4_correlations"]
        if correlations.get("multicollinearity_issues", 0) > 0:
            recommendations.append(
                {
                    "category": "Feature Engineering",
                    "priority": "High",
                    "recommendation": f"{correlations['multicollinearity_issues']} features with high VIF",
                    "actions": [
                        "Remove or combine highly correlated features",
                        "Use PCA for dimensionality reduction",
                    ],
                }
            )

        # ML Readiness Recommendations
        ml_readiness = results["phase5_ml_readiness"]
        if ml_readiness.get("overall_score", 0) < 70:
            recommendations.append(
                {
                    "category": "ML Preparation",
                    "priority": "High",
                    "recommendation": "Dataset not ready for ML",
                    "actions": [
                        "Apply recommended transformations",
                        "Handle missing data",
                        "Address imbalance",
                    ],
                }
            )

        # Leakage Detection
        leakage = ml_readiness.get("leakage_detection", {})
        if leakage.get("leakage_detected"):
            recommendations.append(
                {
                    "category": "Data Leakage",
                    "priority": "Critical",
                    "recommendation": f"{leakage.get('count', 0)} potential leakage features detected",
                    "actions": [
                        f"Remove feature: {s['feature']}"
                        for s in leakage.get("suspects", [])
                    ],
                }
            )

        return recommendations

    def get_quick_summary(self) -> str:
        """Get quick text summary"""
        results = self.run_complete_analysis()
        summary = results["executive_summary"]

        text = f"""
╔══════════════════════════════════════════════════════════════╗
║           ENTERPRISE EDA - EXECUTIVE SUMMARY                 ║
╚══════════════════════════════════════════════════════════════╝

📊 Dataset: {summary['dataset_shape']}

🎯 DATA RELIABILITY INDEX (DRI)
   Score: {summary['dri_score']}/100
   Grade: {summary['dri_grade']}

🏗️ STRUCTURAL QUALITY
   Schema Score: {summary['schema_quality']}/100
   Primary Keys: {len(summary['primary_keys'])} detected

📈 STATISTICAL ANALYSIS
   Non-normal distributions: {summary['non_normal_features']}

🔗 CORRELATIONS
   High correlations: {summary['high_correlations']}
   Multicollinearity issues: {summary['multicollinearity_issues']}

🤖 ML READINESS
   Score: {summary['ml_readiness_score']}/100
   Grade: {summary['ml_readiness_grade']}

⚠️ CRITICAL ISSUES
"""
        for issue in summary["critical_issues"]:
            text += f"   • {issue}\n"

        text += "\n📋 RECOMMENDATIONS\n"
        for rec in results["recommendations"][:5]:
            text += f"   [{rec['priority']}] {rec['recommendation']}\n"

        return text
