"""
Test script to verify all 5 phases of Enterprise EDA are working
"""
import pandas as pd
import numpy as np
from backend.eda.enterprise_eda import EnterpriseEDA

# Create sample dataset
np.random.seed(42)
n_samples = 1000

df = pd.DataFrame({
    'id': range(n_samples),
    'age': np.random.randint(18, 80, n_samples),
    'income': np.random.normal(50000, 15000, n_samples),
    'credit_score': np.random.randint(300, 850, n_samples),
    'loan_amount': np.random.normal(20000, 5000, n_samples),
    'employment_years': np.random.randint(0, 40, n_samples),
    'debt_ratio': np.random.uniform(0, 1, n_samples),
    'category': np.random.choice(['A', 'B', 'C'], n_samples),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
    'default': np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
})

# Add some missing values
df.loc[np.random.choice(df.index, 50), 'income'] = np.nan
df.loc[np.random.choice(df.index, 30), 'credit_score'] = np.nan

print("=" * 80)
print("TESTING ENTERPRISE EDA - ALL 5 PHASES")
print("=" * 80)
print(f"\n📊 Test Dataset: {df.shape[0]} rows × {df.shape[1]} columns\n")

# Initialize Enterprise EDA
eda = EnterpriseEDA(df, target_col='default')

# Run complete analysis
print("🚀 Running complete analysis...\n")
results = eda.run_complete_analysis()

print("\n" + "=" * 80)
print("VERIFICATION RESULTS")
print("=" * 80)

# Verify Phase 1
print("\n✅ PHASE 1: Data Quality (DRI)")
phase1 = results.get('phase1_data_quality', {})
if phase1:
    print(f"   - DRI Score: {phase1.get('dri_score', 'N/A')}/100")
    print(f"   - Grade: {phase1.get('grade', 'N/A')}")
    print(f"   - Components: {len(phase1.get('component_scores', {}))}")
    print("   ✓ Phase 1 WORKING")
else:
    print("   ✗ Phase 1 FAILED")

# Verify Phase 2
print("\n✅ PHASE 2: Structural Analysis")
phase2 = results.get('phase2_structural', {})
if phase2:
    print(f"   - Column Types: {len(phase2.get('column_types', {}))}")
    print(f"   - Primary Keys: {phase2.get('primary_keys', [])}")
    print(f"   - Schema Quality: {phase2.get('schema_quality', {}).get('quality_score', 'N/A')}/100")
    print("   ✓ Phase 2 WORKING")
else:
    print("   ✗ Phase 2 FAILED")

# Verify Phase 3
print("\n✅ PHASE 3: Statistical Analysis")
phase3 = results.get('phase3_statistical', {})
if phase3:
    print(f"   - Numerical Analysis: {len(phase3.get('numerical_analysis', {}))}")
    print(f"   - Categorical Analysis: {len(phase3.get('categorical_analysis', {}))}")
    print(f"   - Summary Stats: {len(phase3.get('summary', {}))}")
    print("   ✓ Phase 3 WORKING")
else:
    print("   ✗ Phase 3 FAILED")

# Verify Phase 4
print("\n✅ PHASE 4: Correlation Analysis")
phase4 = results.get('phase4_correlations', {})
if phase4:
    print(f"   - Pearson High Corr: {phase4.get('pearson_high_count', 0)}")
    print(f"   - Spearman High Corr: {phase4.get('spearman_high_count', 0)}")
    print(f"   - VIF Issues: {phase4.get('multicollinearity_issues', 0)}")
    print("   ✓ Phase 4 WORKING")
else:
    print("   ✗ Phase 4 FAILED")

# Verify Phase 5
print("\n✅ PHASE 5: ML Readiness")
phase5 = results.get('phase5_ml_readiness', {})
if phase5:
    print(f"   - Overall Score: {phase5.get('overall_score', 'N/A')}/100")
    print(f"   - Readiness Grade: {phase5.get('readiness_grade', 'N/A')}")
    print(f"   - Leakage Detected: {phase5.get('leakage_detection', {}).get('leakage_detected', False)}")
    print("   ✓ Phase 5 WORKING")
else:
    print("   ✗ Phase 5 FAILED")

# Verify Executive Summary
print("\n✅ EXECUTIVE SUMMARY")
summary = results.get('executive_summary', {})
if summary:
    print(f"   - DRI Score: {summary.get('dri_score', 'N/A')}/100")
    print(f"   - ML Readiness: {summary.get('ml_readiness_score', 'N/A')}/100")
    print(f"   - Critical Issues: {len(summary.get('critical_issues', []))}")
    print("   ✓ Executive Summary WORKING")
else:
    print("   ✗ Executive Summary FAILED")

# Verify Recommendations
print("\n✅ RECOMMENDATIONS")
recommendations = results.get('recommendations', [])
if recommendations:
    print(f"   - Total Recommendations: {len(recommendations)}")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
    print("   ✓ Recommendations WORKING")
else:
    print("   ✗ Recommendations FAILED")

# Final Summary
print("\n" + "=" * 80)
print("FINAL VERIFICATION")
print("=" * 80)

all_phases_working = all([
    results.get('phase1_data_quality'),
    results.get('phase2_structural'),
    results.get('phase3_statistical'),
    results.get('phase4_correlations'),
    results.get('phase5_ml_readiness'),
    results.get('executive_summary'),
    results.get('recommendations')
])

if all_phases_working:
    print("\n🎉 SUCCESS! All 5 phases are properly integrated and working!")
    print("\n✅ Phase 1: Data Quality (DRI) - WORKING")
    print("✅ Phase 2: Structural Analysis - WORKING")
    print("✅ Phase 3: Statistical Analysis - WORKING")
    print("✅ Phase 4: Correlation Analysis - WORKING")
    print("✅ Phase 5: ML Readiness - WORKING")
    print("✅ Executive Summary - WORKING")
    print("✅ Recommendations - WORKING")
    print("\n🚀 Enterprise EDA system is fully operational!")
else:
    print("\n❌ FAILURE! Some phases are not working properly.")
    print("Please check the error messages above.")

print("\n" + "=" * 80)
