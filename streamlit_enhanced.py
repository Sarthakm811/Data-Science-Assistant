import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import google.generativeai as genai
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, r2_score, mean_squared_error
import os
import sys
from datetime import datetime
import json

# Kaggle API will be imported only when needed to avoid authentication errors
KaggleApi = None

# Add backend to path for enterprise EDA
sys.path.insert(0, os.path.abspath('.'))

# Import enterprise EDA modules
try:
    from backend.eda.enterprise_eda import EnterpriseEDA
    from backend.eda.enhanced_visualizations import EnhancedVisualizer
    ENTERPRISE_EDA_AVAILABLE = True
except ImportError:
    ENTERPRISE_EDA_AVAILABLE = False
    print("⚠️ Enterprise EDA modules not available")

# Page config
st.set_page_config(
    page_title="AI Data Science Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'datasets' not in st.session_state:
    st.session_state.datasets = []
if 'selected_dataset' not in st.session_state:
    st.session_state.selected_dataset = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'eda_run' not in st.session_state:
    st.session_state.eda_run = False

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get default values from environment
DEFAULT_GEMINI_KEY = os.getenv('GEMINI_API_KEY', '')
DEFAULT_KAGGLE_USERNAME = os.getenv('KAGGLE_USERNAME', '')
DEFAULT_KAGGLE_KEY = os.getenv('KAGGLE_KEY', '')

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.info("🔐 **Setup Required:** Enter your API credentials below")
    
    gemini_key = st.text_input("Gemini API Key", 
                                value=DEFAULT_GEMINI_KEY,
                                type="password", 
                                help="Get from https://makersuite.google.com/app/apikey",
                                placeholder="Enter your Gemini API key")
    kaggle_username = st.text_input("Kaggle Username", 
                                     value=DEFAULT_KAGGLE_USERNAME,
                                     help="Get from https://www.kaggle.com/settings/account",
                                     placeholder="Enter your Kaggle username")
    kaggle_key = st.text_input("Kaggle API Key", 
                                value=DEFAULT_KAGGLE_KEY,
                                type="password",
                                help="Get from https://www.kaggle.com/settings/account",
                                placeholder="Enter your Kaggle API key")
    
    if gemini_key:
        genai.configure(api_key=gemini_key)
    
    st.caption("🔒 Your credentials are stored only in this session and never saved to disk")
    
    st.divider()
    
    # Dataset Upload
    st.header("📁 Upload Dataset")
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    
    if uploaded_file:
        try:
            st.session_state.df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            # Try alternative encodings
            for encoding in ['latin-1', 'iso-8859-1', 'cp1252', 'utf-16']:
                try:
                    uploaded_file.seek(0)  # Reset file pointer
                    st.session_state.df = pd.read_csv(uploaded_file, encoding=encoding)
                    st.info(f"✓ File loaded with {encoding} encoding")
                    break
                except:
                    continue
            else:
                st.error("Could not decode file with any supported encoding")
                st.session_state.df = None
        
        if st.session_state.df is not None:
            st.session_state.selected_dataset = uploaded_file.name
            st.success(f"Loaded: {uploaded_file.name}")
            st.info(f"Shape: {st.session_state.df.shape}")
    
    # Show current dataset status
    st.divider()
    if st.session_state.df is not None:
        st.success(f"✅ Dataset Loaded")
        st.write(f"**Name:** {st.session_state.selected_dataset or 'Unknown'}")
        st.write(f"**Shape:** {st.session_state.df.shape[0]} rows × {st.session_state.df.shape[1]} cols")
        if st.button("🗑️ Clear Dataset"):
            st.session_state.df = None
            st.session_state.selected_dataset = None
            st.session_state.eda_run = False
            st.rerun()
    else:
        st.warning("⚠️ No dataset loaded")

# Main Header
st.markdown('<h1 class="main-header">🤖 AI Data Science Research Assistant</h1>', 
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Your Personal AI Data Scientist</p>", 
            unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🔍 Dataset Search", 
    "📊 Auto EDA", 
    "🤖 Auto ML", 
    "💬 AI Chat", 
    "📄 Reports",
    "📈 Advanced Statistics",
    "🎨 3D Visualization",
    "🧹 Data Processing",
    "🎯 Anomaly Detection"
])

# Tab 1: Dataset Search
with tab1:
    st.header("🔍 Search Kaggle Datasets")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search datasets", 
                                     placeholder="e.g., housing, titanic, sales")
    with col2:
        search_btn = st.button("🔎 Search", use_container_width=True)
    
    if search_btn and search_query and kaggle_username and kaggle_key:
        with st.spinner("Searching Kaggle..."):
            try:
                # Import Kaggle API only when needed
                from kaggle.api.kaggle_api_extended import KaggleApi
                
                os.environ['KAGGLE_USERNAME'] = kaggle_username
                os.environ['KAGGLE_KEY'] = kaggle_key
                
                api = KaggleApi()
                api.authenticate()
                
                datasets = api.dataset_list(search=search_query, page=1)
                st.session_state.datasets = datasets[:10]
                
                st.success(f"Found {len(st.session_state.datasets)} datasets")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display datasets
    if st.session_state.datasets:
        st.subheader("📋 Search Results")
        
        for idx, ds in enumerate(st.session_state.datasets):
            with st.expander(f"📊 {ds.title}"):
                st.write(f"**ID:** {ds.ref}")
                if hasattr(ds, 'totalBytes'):
                    size_mb = ds.totalBytes / (1024 * 1024)
                    st.write(f"**Size:** {size_mb:.2f} MB")
                st.write(f"**URL:** https://www.kaggle.com/datasets/{ds.ref}")
                
                if st.button(f"📥 Download & Load", key=f"load_{idx}"):
                    with st.spinner("📥 Downloading dataset from Kaggle..."):
                        try:
                            # Import Kaggle API only when needed
                            from kaggle.api.kaggle_api_extended import KaggleApi
                            
                            # Re-authenticate for download
                            os.environ['KAGGLE_USERNAME'] = kaggle_username
                            os.environ['KAGGLE_KEY'] = kaggle_key
                            
                            download_api = KaggleApi()
                            download_api.authenticate()
                            
                            # Create data directory if it doesn't exist
                            os.makedirs('./data', exist_ok=True)
                            
                            # Clear old files from data directory
                            import glob
                            import shutil
                            for old_file in glob.glob('./data/*'):
                                try:
                                    if os.path.isfile(old_file):
                                        os.remove(old_file)
                                    elif os.path.isdir(old_file):
                                        shutil.rmtree(old_file)
                                except:
                                    pass
                            
                            # Download dataset
                            st.info(f"Downloading {ds.ref}...")
                            download_api.dataset_download_files(ds.ref, path='./data', unzip=True)
                            
                            # Find CSV file
                            csv_files = glob.glob('./data/*.csv')
                            
                            if csv_files:
                                # Sort by size (largest first) to get the main dataset
                                csv_files.sort(key=lambda x: os.path.getsize(x), reverse=True)
                                selected_file = csv_files[0]
                                
                                st.info(f"Loading {os.path.basename(selected_file)}...")
                                
                                # Load the dataset with encoding detection
                                try:
                                    df_new = pd.read_csv(selected_file)
                                except UnicodeDecodeError:
                                    # Try alternative encodings
                                    for encoding in ['latin-1', 'iso-8859-1', 'cp1252', 'utf-16']:
                                        try:
                                            df_new = pd.read_csv(selected_file, encoding=encoding)
                                            st.info(f"✓ File loaded with {encoding} encoding")
                                            break
                                        except:
                                            continue
                                    else:
                                        raise ValueError("Could not decode file with any supported encoding")
                                
                                # Store in session state
                                st.session_state.df = df_new
                                st.session_state.selected_dataset = ds.title
                                st.session_state.selected_dataset_ref = ds.ref
                                
                                # Show success message with balloons
                                st.balloons()
                                st.success(f"""
                                ✅ **Dataset Successfully Downloaded and Loaded!**
                                
                                📊 **Dataset:** {ds.title}
                                📁 **File:** {os.path.basename(selected_file)}
                                📏 **Shape:** {df_new.shape[0]} rows × {df_new.shape[1]} columns
                                💾 **Size:** {df_new.memory_usage(deep=True).sum() / 1024**2:.2f} MB
                                
                                🎉 Ready for analysis! Go to the **Auto EDA** or **Auto ML** tab to start.
                                """)
                                
                                st.info("✨ Dataset is now loaded and ready in all tabs!")
                                
                                # Verify it's in session state
                                st.write(f"**Verification:** Dataset stored with {len(st.session_state.df)} rows")
                                
                                # Wait a moment before rerun
                                import time
                                time.sleep(1)
                                
                                # Force rerun to update UI
                                st.rerun()
                                
                            else:
                                st.warning("⚠️ No CSV files found in the downloaded dataset.")
                                
                        except Exception as e:
                            st.error(f"❌ **Download Failed:** {str(e)}")
                            st.info("💡 **Tip:** Check your Kaggle credentials and internet connection.")
                            st.exception(e)

# Tab 2: Auto EDA
with tab2:
    st.header("📊 Automated Exploratory Data Analysis")
    
    # Debug info
    # st.write(f"DEBUG: df is None? {st.session_state.df is None}")
    
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # Show current dataset info
        st.info(f"📊 **Current Dataset:** {st.session_state.selected_dataset or 'Uploaded File'} | "
                f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns | "
                f"**Memory:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Analysis mode selection
        analysis_mode = st.radio(
            "Analysis Mode",
            ["🚀 Quick EDA", "🏢 Enterprise EDA (Advanced)"],
            horizontal=True
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚀 Run Analysis", use_container_width=True, type="primary"):
                st.session_state.eda_run = True
        
        with col2:
            target_col_eda = st.selectbox("Target Column (optional)", 
                                          ["None"] + df.columns.tolist(),
                                          key="eda_target")
        
        with col3:
            if st.session_state.eda_run:
                if st.button("🔄 Reset Analysis", use_container_width=True):
                    st.session_state.eda_run = False
                    st.rerun()
        
        if st.session_state.eda_run:
            if "Enterprise" in analysis_mode and ENTERPRISE_EDA_AVAILABLE:
                # ENTERPRISE EDA
                with st.spinner("🏢 Running Enterprise-Grade Analysis..."):
                    target = None if target_col_eda == "None" else target_col_eda
                    
                    enterprise_eda = EnterpriseEDA(df, target)
                    results = enterprise_eda.run_complete_analysis()
                    
                    # Display Executive Summary
                    st.success("✅ Enterprise EDA Complete!")
                    
                    with st.expander("📊 EXECUTIVE SUMMARY", expanded=True):
                        summary = results['executive_summary']
                        
                        col_a, col_b, col_c, col_d = st.columns(4)
                        col_a.metric("DRI Score", f"{summary['dri_score']}/100", 
                                    delta=summary['dri_grade'])
                        col_b.metric("Schema Quality", f"{summary['schema_quality']}/100")
                        col_c.metric("ML Readiness", f"{summary['ml_readiness_score']}/100")
                        col_d.metric("High Correlations", summary['high_correlations'])
                        
                        st.markdown("**Critical Issues:**")
                        for issue in summary['critical_issues']:
                            st.markdown(f"- {issue}")
                    
                    # Phase 1: Data Quality
                    with st.expander("🎯 PHASE 1: Data Reliability Index (DRI)"):
                        dri = results['phase1_data_quality']
                        
                        st.markdown(f"### DRI Score: **{dri['dri_score']}/100** - {dri['grade']}")
                        
                        # Component scores
                        st.markdown("#### Component Scores:")
                        comp_df = pd.DataFrame([dri['component_scores']]).T
                        comp_df.columns = ['Score']
                        st.dataframe(comp_df, use_container_width=True)
                        
                        # Visualize with Plotly gauge
                        if hasattr(enterprise_eda.visualizer, 'create_quality_scorecard'):
                            fig = enterprise_eda.visualizer.create_quality_scorecard(dri)
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                    
                    # Phase 2: Structural Analysis
                    with st.expander("🏗️ PHASE 2: Structural Analysis"):
                        structural = results['phase2_structural']
                        
                        st.markdown("#### Column Types (Semantic Inference):")
                        col_types = structural.get('column_types', {})
                        types_df = pd.DataFrame([
                            {
                                'Column': col,
                                'Semantic Type': data['semantic_type'],
                                'Confidence': f"{data['confidence']:.0%}"
                            }
                            for col, data in col_types.items()
                        ])
                        st.dataframe(types_df, use_container_width=True)
                        
                        st.markdown("#### Primary Keys:")
                        pks = structural.get('primary_keys', [])
                        if pks:
                            st.success(f"✅ Detected: {', '.join(pks)}")
                        else:
                            st.warning("⚠️ No primary key detected")
                        
                        st.markdown("#### Relationships:")
                        relationships = structural.get('relationships', {})
                        for rel_type, rels in relationships.items():
                            if rels:
                                st.write(f"**{rel_type.replace('_', ' ').title()}:** {len(rels)} detected")
                    
                    # Phase 3: Statistical Analysis
                    with st.expander("📈 PHASE 3: Statistical Analysis"):
                        statistical = results['phase3_statistical']
                        
                        st.markdown("#### Numerical Features Analysis:")
                        num_analysis = statistical.get('numerical_analysis', {})
                        
                        for col, analysis in list(num_analysis.items())[:5]:
                            st.markdown(f"**{col}:**")
                            col_a, col_b, col_c = st.columns(3)
                            col_a.metric("Skewness", f"{analysis['skewness']:.2f}")
                            col_b.metric("Kurtosis", f"{analysis['kurtosis']:.2f}")
                            
                            normality = analysis.get('normality_tests', {})
                            if 'shapiro_wilk' in normality:
                                is_normal = "✅ Normal" if normality['shapiro_wilk']['is_normal'] else "❌ Not Normal"
                                col_c.metric("Normality", is_normal)
                        
                        st.markdown("#### Categorical Features Analysis:")
                        cat_analysis = statistical.get('categorical_analysis', {})
                        
                        for col, analysis in list(cat_analysis.items())[:5]:
                            st.markdown(f"**{col}:**")
                            imbalance = analysis.get('imbalance', {})
                            if imbalance:
                                st.write(f"- Imbalance: {imbalance.get('severity', 'N/A')}")
                                st.write(f"- Majority: {imbalance.get('majority_percentage', 0):.1f}%")
                    
                    # Phase 4: Correlations
                    with st.expander("🔗 PHASE 4: Correlation Analysis"):
                        st.markdown("#### Correlation Summary:")
                        corr_summary = results['phase4_correlations']
                        
                        col_a, col_b, col_c = st.columns(3)
                        col_a.metric("Pearson High Corr", corr_summary.get('pearson_high_count', 0))
                        col_b.metric("Spearman High Corr", corr_summary.get('spearman_high_count', 0))
                        col_c.metric("VIF Issues", corr_summary.get('multicollinearity_issues', 0))
                        
                        if corr_summary.get('redundant_features', 0) > 0:
                            st.warning(f"⚠️ {corr_summary['redundant_features']} redundant features detected")
                    
                    # Phase 5: ML Readiness
                    with st.expander("🤖 PHASE 5: ML Readiness Assessment"):
                        ml_readiness = results['phase5_ml_readiness']
                        
                        st.markdown(f"### ML Readiness: **{ml_readiness.get('overall_score', 0)}/100**")
                        st.markdown(f"**Grade:** {ml_readiness.get('readiness_grade', 'N/A')}")
                        
                        # Feature scores
                        if 'feature_scores' in ml_readiness:
                            st.markdown("#### Top Features:")
                            top_features = ml_readiness['feature_scores'].get('top_features', [])
                            if top_features:
                                feat_df = pd.DataFrame(top_features)
                                st.dataframe(feat_df, use_container_width=True)
                        
                        # Leakage detection
                        leakage = ml_readiness.get('leakage_detection', {})
                        if leakage.get('leakage_detected'):
                            st.error(f"🚨 **Target Leakage Detected:** {leakage.get('count', 0)} suspects")
                            for suspect in leakage.get('suspects', []):
                                st.warning(f"- {suspect['feature']}: {suspect['reason']}")
                        
                        # Imbalance
                        imbalance = ml_readiness.get('imbalance_analysis', {})
                        if imbalance.get('imbalanced'):
                            st.warning(f"⚠️ **Class Imbalance:** {imbalance.get('severity', 'N/A')}")
                            st.write(f"Ratio: {imbalance.get('imbalance_ratio', 0):.2f}:1")
                            if imbalance.get('smote_recommended'):
                                st.info(f"💡 SMOTE recommended: Generate {imbalance.get('samples_to_generate', 0)} samples")
                    
                    # Recommendations
                    with st.expander("📋 ACTIONABLE RECOMMENDATIONS", expanded=True):
                        recommendations = results['recommendations']
                        
                        for rec in recommendations:
                            priority_color = {
                                'Critical': '🔴',
                                'High': '🟠',
                                'Medium': '🟡',
                                'Low': '🟢'
                            }.get(rec['priority'], '⚪')
                            
                            st.markdown(f"### {priority_color} {rec['category']} - {rec['priority']} Priority")
                            st.markdown(f"**{rec['recommendation']}**")
                            st.markdown("**Actions:**")
                            for action in rec['actions']:
                                st.markdown(f"- {action}")
                            st.divider()
                    
                    # ENHANCED VISUALIZATIONS
                    st.markdown("---")
                    st.markdown("## 📊 INTERACTIVE VISUALIZATIONS")
                    
                    viz = EnhancedVisualizer(df, target)
                    
                    # Create visualization tabs
                    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
                        "📈 Dataset Overview",
                        "📉 Distributions",
                        "🔗 Correlations",
                        "📊 Categories"
                    ])
                    
                    with viz_tab1:
                        st.subheader("Dataset Overview")
                        
                        # Debug info
                        st.info(f"📊 Analyzing: {df.shape[0]} rows × {df.shape[1]} columns | Missing values: {df.isnull().sum().sum()}")
                        
                        col_v1, col_v2 = st.columns(2)
                        
                        with col_v1:
                            st.plotly_chart(viz.create_data_type_summary(), use_container_width=True)
                        
                        with col_v2:
                            st.plotly_chart(viz.create_missing_data_bar(), use_container_width=True)
                        
                        st.plotly_chart(viz.create_missing_data_heatmap(), use_container_width=True)
                    
                    with viz_tab2:
                        st.subheader("Distribution Analysis")
                        
                        if viz.numeric_cols:
                            # Initialize session state for selected column
                            if 'dist_col_enterprise' not in st.session_state:
                                st.session_state.dist_col_enterprise = viz.numeric_cols[0]
                            
                            selected_num_col = st.selectbox(
                                "Select Numerical Column",
                                viz.numeric_cols,
                                index=viz.numeric_cols.index(st.session_state.dist_col_enterprise) if st.session_state.dist_col_enterprise in viz.numeric_cols else 0,
                                key="dist_col_enterprise_select"
                            )
                            
                            # Update session state
                            st.session_state.dist_col_enterprise = selected_num_col
                            
                            col_d1, col_d2 = st.columns(2)
                            
                            with col_d1:
                                st.plotly_chart(viz.create_distribution_plot(selected_num_col), use_container_width=True)
                            
                            with col_d2:
                                st.plotly_chart(viz.create_violin_plot(selected_num_col), use_container_width=True)
                            
                            st.plotly_chart(viz.create_outlier_detection_plot(selected_num_col), use_container_width=True)
                        else:
                            st.info("No numerical columns available for distribution analysis")
                    
                    with viz_tab3:
                        st.subheader("Correlation Analysis")
                        
                        if len(viz.numeric_cols) >= 2:
                            # Initialize session state
                            if 'corr_method_enterprise' not in st.session_state:
                                st.session_state.corr_method_enterprise = "pearson"
                            if 'show_scatter_enterprise' not in st.session_state:
                                st.session_state.show_scatter_enterprise = False
                            
                            corr_method = st.radio(
                                "Correlation Method",
                                ["pearson", "spearman"],
                                index=0 if st.session_state.corr_method_enterprise == "pearson" else 1,
                                horizontal=True,
                                key="corr_method_enterprise_radio"
                            )
                            
                            # Update session state
                            st.session_state.corr_method_enterprise = corr_method
                            
                            # Display correlation heatmap
                            with st.spinner(f"Calculating {corr_method} correlation..."):
                                corr_fig = viz.create_correlation_heatmap(corr_method)
                                st.plotly_chart(corr_fig, use_container_width=True, key=f"corr_heatmap_enterprise_{corr_method}")
                            
                            # Target correlation
                            if target:
                                target_corr_fig = viz.create_correlation_with_target()
                                if target_corr_fig:
                                    st.plotly_chart(target_corr_fig, use_container_width=True)
                            
                            # Scatter matrix
                            st.divider()
                            show_scatter = st.checkbox(
                                "Show Scatter Matrix (may be slow for large datasets)", 
                                value=st.session_state.show_scatter_enterprise,
                                key="scatter_matrix_enterprise_check"
                            )
                            
                            # Update session state
                            st.session_state.show_scatter_enterprise = show_scatter
                            
                            if show_scatter:
                                with st.spinner("Generating scatter matrix..."):
                                    scatter_fig = viz.create_scatter_matrix(max_cols=5)
                                    if scatter_fig:
                                        st.plotly_chart(scatter_fig, use_container_width=True)
                                    else:
                                        st.warning("Could not generate scatter matrix")
                        else:
                            st.info("Need at least 2 numerical columns for correlation analysis")
                    
                    with viz_tab4:
                        st.subheader("Categorical Analysis")
                        
                        if viz.categorical_cols:
                            # Initialize session state
                            if 'cat_col_enterprise' not in st.session_state:
                                st.session_state.cat_col_enterprise = viz.categorical_cols[0]
                            
                            selected_cat_col = st.selectbox(
                                "Select Categorical Column",
                                viz.categorical_cols,
                                index=viz.categorical_cols.index(st.session_state.cat_col_enterprise) if st.session_state.cat_col_enterprise in viz.categorical_cols else 0,
                                key="cat_col_enterprise_select"
                            )
                            
                            # Update session state
                            st.session_state.cat_col_enterprise = selected_cat_col
                            
                            col_c1, col_c2 = st.columns(2)
                            
                            with col_c1:
                                st.plotly_chart(viz.create_category_bar_chart(selected_cat_col), use_container_width=True)
                            
                            with col_c2:
                                st.plotly_chart(viz.create_category_pie_chart(selected_cat_col), use_container_width=True)
                            
                            if target:
                                target_rel_fig = viz.create_category_target_relationship(selected_cat_col)
                                if target_rel_fig:
                                    st.plotly_chart(target_rel_fig, use_container_width=True)
                        else:
                            st.info("No categorical columns available for analysis")
            
            else:
                # QUICK EDA with Enhanced Visualizations
                # Initialize visualizer
                target = None if target_col_eda == "None" else target_col_eda
                viz = EnhancedVisualizer(df, target) if ENTERPRISE_EDA_AVAILABLE else None
                
                # Basic Info
                st.subheader("📋 Dataset Overview")
                col_a, col_b, col_c, col_d = st.columns(4)
                col_a.metric("Rows", df.shape[0])
                col_b.metric("Columns", df.shape[1])
                col_c.metric("Numeric", len(df.select_dtypes(include=[np.number]).columns))
                col_d.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
                
                # Data Type Distribution
                if viz:
                    st.info(f"📊 Analyzing: {df.shape[0]} rows × {df.shape[1]} columns | Missing values: {df.isnull().sum().sum()}")
                    col_viz1, col_viz2 = st.columns(2)
                    with col_viz1:
                        st.plotly_chart(viz.create_data_type_summary(), use_container_width=True)
                    with col_viz2:
                        st.plotly_chart(viz.create_missing_data_bar(), use_container_width=True)
                
                # Summary Stats
                st.subheader("📈 Summary Statistics")
                st.dataframe(df.describe(), use_container_width=True)
                
                # Missing Data Analysis
                st.subheader("⚠️ Missing Data Analysis")
                missing = df.isnull().sum()
                missing_pct = (missing / len(df)) * 100
                missing_df = pd.DataFrame({
                    'Missing Count': missing[missing > 0],
                    'Percentage': missing_pct[missing > 0]
                })
                
                if not missing_df.empty:
                    col_m1, col_m2 = st.columns([1, 2])
                    with col_m1:
                        st.dataframe(missing_df, use_container_width=True)
                    with col_m2:
                        if viz:
                            st.plotly_chart(viz.create_missing_data_heatmap(), use_container_width=True)
                else:
                    st.success("✅ No missing data!")
                
                # Correlations
                numeric_df = df.select_dtypes(include=[np.number])
                if numeric_df.shape[1] >= 2:
                    st.subheader("🔗 Correlation Analysis")
                    
                    if viz:
                        # Initialize session state
                        if 'corr_method_quick' not in st.session_state:
                            st.session_state.corr_method_quick = "pearson"
                        if 'show_scatter_quick' not in st.session_state:
                            st.session_state.show_scatter_quick = False
                        
                        corr_method_quick = st.radio(
                            "Correlation Method",
                            ["pearson", "spearman"],
                            index=0 if st.session_state.corr_method_quick == "pearson" else 1,
                            horizontal=True,
                            key="corr_method_quick_radio"
                        )
                        
                        # Update session state
                        st.session_state.corr_method_quick = corr_method_quick
                        
                        with st.spinner(f"Calculating {corr_method_quick} correlation..."):
                            corr_fig = viz.create_correlation_heatmap(corr_method_quick)
                            st.plotly_chart(corr_fig, use_container_width=True, key=f"corr_heatmap_quick_{corr_method_quick}")
                        
                        if target and target in numeric_df.columns:
                            target_corr_fig = viz.create_correlation_with_target()
                            if target_corr_fig:
                                st.plotly_chart(target_corr_fig, use_container_width=True)
                        
                        # Scatter matrix option
                        show_scatter_quick = st.checkbox(
                            "Show Scatter Matrix", 
                            value=st.session_state.show_scatter_quick,
                            key="scatter_matrix_quick_check"
                        )
                        
                        # Update session state
                        st.session_state.show_scatter_quick = show_scatter_quick
                        
                        if show_scatter_quick:
                            with st.spinner("Generating scatter matrix..."):
                                scatter_fig = viz.create_scatter_matrix(max_cols=5)
                                if scatter_fig:
                                    st.plotly_chart(scatter_fig, use_container_width=True)
                    else:
                        fig, ax = plt.subplots(figsize=(12, 10))
                        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', 
                                   center=0, fmt='.2f', ax=ax)
                        ax.set_title('Correlation Heatmap')
                        st.pyplot(fig)
                
                # Distributions
                st.subheader("📉 Distribution Analysis")
                if not numeric_df.empty:
                    if viz:
                        # Interactive distribution plots
                        selected_cols = st.multiselect(
                            "Select columns to visualize",
                            numeric_df.columns.tolist(),
                            default=numeric_df.columns.tolist()[:3],
                            key="quick_dist_cols"
                        )
                        
                        for col in selected_cols:
                            with st.expander(f"📊 {col}", expanded=len(selected_cols) <= 3):
                                col_d1, col_d2 = st.columns(2)
                                with col_d1:
                                    st.plotly_chart(viz.create_distribution_plot(col), use_container_width=True)
                                with col_d2:
                                    st.plotly_chart(viz.create_violin_plot(col), use_container_width=True)
                    else:
                        # Fallback to matplotlib
                        n_cols = min(3, len(numeric_df.columns))
                        cols = st.columns(n_cols)
                        
                        for idx, col in enumerate(numeric_df.columns[:6]):
                            with cols[idx % n_cols]:
                                fig, ax = plt.subplots(figsize=(5, 3))
                                numeric_df[col].hist(bins=30, ax=ax, edgecolor='black')
                                ax.set_title(f'{col}')
                                st.pyplot(fig)
                
                # Outlier Detection
                st.subheader("📦 Outlier Detection")
                if not numeric_df.empty:
                    if viz:
                        outlier_col = st.selectbox(
                            "Select column for outlier analysis",
                            numeric_df.columns.tolist(),
                            key="outlier_col"
                        )
                        st.plotly_chart(viz.create_outlier_detection_plot(outlier_col), use_container_width=True)
                    else:
                        if len(numeric_df.columns) <= 10:
                            fig, ax = plt.subplots(figsize=(12, 6))
                            numeric_df.boxplot(ax=ax)
                            ax.set_title('Box Plots')
                            plt.xticks(rotation=45, ha='right')
                            st.pyplot(fig)
                
                # Categorical Analysis
                categorical_df = df.select_dtypes(include=['object', 'category'])
                if not categorical_df.empty:
                    st.subheader("📊 Categorical Analysis")
                    
                    if viz:
                        cat_col = st.selectbox(
                            "Select categorical column",
                            categorical_df.columns.tolist(),
                            key="cat_analysis_col"
                        )
                        
                        col_cat1, col_cat2 = st.columns(2)
                        with col_cat1:
                            st.plotly_chart(viz.create_category_bar_chart(cat_col), use_container_width=True)
                        with col_cat2:
                            st.plotly_chart(viz.create_category_pie_chart(cat_col), use_container_width=True)
                        
                        if target and target in numeric_df.columns:
                            target_rel = viz.create_category_target_relationship(cat_col)
                            if target_rel:
                                st.plotly_chart(target_rel, use_container_width=True)
                
                st.success("✅ EDA Complete!")
                
                # Data Preview
                st.subheader("👀 Data Preview")
                st.dataframe(df.head(10))
        
    else:
        st.info("👆 Upload a dataset or search Kaggle to get started!")

# Tab 3: Auto ML
with tab3:
    st.header("🤖 Automated Machine Learning")
    
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # Show current dataset info
        st.info(f"📊 **Current Dataset:** {st.session_state.selected_dataset or 'Uploaded File'} | "
                f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns | "
                f"**Memory:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Show dataset info
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Dataset", "Loaded ✅")
        
        st.subheader("🎯 Select Target Variable")
        
        # Only show numeric columns for target
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            st.error("❌ No numeric columns found! Please upload a dataset with numeric features.")
        else:
            target_col = st.selectbox("Target Column (must be numeric)", numeric_cols)
            
            task_type = st.radio("Task Type", ["Auto Detect", "Classification", "Regression"])
            
            if st.button("🚀 Train Models", use_container_width=True, type="primary"):
                with st.spinner("🔄 Training models... This may take a moment..."):
                    try:
                        # Show progress
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("📊 Preparing data...")
                        progress_bar.progress(10)
                        
                        # Prepare data
                        X = df.drop(columns=[target_col]).copy()
                        y = df[target_col].copy()
                        
                        # Drop rows with missing target values
                        mask = y.notna()
                        X = X[mask]
                        y = y[mask]
                        
                        st.info(f"📈 Training on {len(X)} samples")
                        
                        # Select only numeric columns for features
                        numeric_features = X.select_dtypes(include=[np.number]).columns
                        
                        if len(numeric_features) == 0:
                            st.error("❌ No numeric features found! Please ensure your dataset has numeric columns besides the target.")
                            st.stop()
                        
                        X = X[numeric_features]
                        
                        st.info(f"📊 Using {len(numeric_features)} numeric features: {', '.join(numeric_features.tolist())}")
                        
                        # Fill missing values
                        for col in X.columns:
                            X[col] = X[col].fillna(X[col].median())
                        
                        if len(X) == 0:
                            st.error("❌ No valid samples remaining after data cleaning!")
                            st.stop()
                        
                        progress_bar.progress(30)
                        status_text.text("🔀 Splitting data...")
                        
                        # Split
                        X_train, X_test, y_train, y_test = train_test_split(
                            X, y, test_size=0.2, random_state=42
                        )
                        
                        # Scale
                        scaler = StandardScaler()
                        X_train_scaled = scaler.fit_transform(X_train)
                        X_test_scaled = scaler.transform(X_test)
                        
                        progress_bar.progress(50)
                        
                        # Detect task
                        if task_type == "Auto Detect":
                            task = "classification" if y.nunique() < 20 else "regression"
                        else:
                            task = task_type.lower()
                        
                        st.info(f"🎯 Task Type: **{task.title()}**")
                        
                        results = {}
                        
                        if task == "classification":
                            status_text.text("🤖 Training classification models...")
                            
                            models = {
                                "Logistic Regression": LogisticRegression(max_iter=1000),
                                "Random Forest": RandomForestClassifier(n_estimators=50, random_state=42)
                            }
                            
                            for idx, (name, model) in enumerate(models.items()):
                                progress_bar.progress(50 + (idx + 1) * 20)
                                model.fit(X_train_scaled, y_train)
                                y_pred = model.predict(X_test_scaled)
                                acc = accuracy_score(y_test, y_pred)
                                results[name] = {"Accuracy": f"{acc:.4f}"}
                        
                        else:
                            status_text.text("🤖 Training regression models...")
                            
                            models = {
                                "Linear Regression": LinearRegression(),
                                "Random Forest": RandomForestRegressor(n_estimators=50, random_state=42)
                            }
                            
                            for idx, (name, model) in enumerate(models.items()):
                                progress_bar.progress(50 + (idx + 1) * 20)
                                model.fit(X_train_scaled, y_train)
                                y_pred = model.predict(X_test_scaled)
                                r2 = r2_score(y_test, y_pred)
                                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                                results[name] = {
                                    "R² Score": f"{r2:.4f}",
                                    "RMSE": f"{rmse:.4f}"
                                }
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Training complete!")
                        
                        # Display results
                        st.subheader("📊 Model Performance")
                        results_df = pd.DataFrame(results).T
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Best model
                        first_metric = results_df.columns[0]
                        results_numeric = results_df[first_metric].astype(float)
                        best_model = results_numeric.idxmax()
                        best_score = results_numeric.max()
                        
                        st.success(f"🏆 **Best Model:** {best_model} ({first_metric}: {best_score:.4f})")
                        
                        # Visualization
                        st.subheader("📈 Model Comparison")
                        fig, ax = plt.subplots(figsize=(10, 6))
                        
                        # Convert to numeric for plotting
                        plot_df = results_df.copy()
                        for col in plot_df.columns:
                            plot_df[col] = plot_df[col].astype(float)
                        
                        plot_df.plot(kind='bar', ax=ax, color=['#667eea', '#764ba2'])
                        ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
                        ax.set_ylabel('Score', fontsize=12)
                        ax.set_xlabel('Model', fontsize=12)
                        plt.xticks(rotation=45, ha='right')
                        plt.legend(title='Metrics')
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                        # Feature importance for Random Forest
                        if 'Random Forest' in models:
                            st.subheader("🎯 Feature Importance (Random Forest)")
                            rf_model = models['Random Forest']
                            rf_model.fit(X_train_scaled, y_train)
                            
                            importance_df = pd.DataFrame({
                                'Feature': X.columns,
                                'Importance': rf_model.feature_importances_
                            }).sort_values('Importance', ascending=False).head(10)
                            
                            fig2, ax2 = plt.subplots(figsize=(10, 6))
                            ax2.barh(importance_df['Feature'], importance_df['Importance'], color='#667eea')
                            ax2.set_xlabel('Importance')
                            ax2.set_title('Top 10 Most Important Features')
                            plt.gca().invert_yaxis()
                            plt.tight_layout()
                            st.pyplot(fig2)
                        
                        st.session_state.analysis_results['ml'] = results
                        
                        # Clear progress
                        progress_bar.empty()
                        status_text.empty()
                        
                    except Exception as e:
                        st.error(f"❌ Error during training: {str(e)}")
                        st.info("💡 Tips: Make sure your target column is numeric and the dataset has enough samples.")
                        with st.expander("🔍 See full error details"):
                            st.exception(e)
    else:
        st.info("👆 Please upload a dataset or search Kaggle datasets first!")

# Tab 4: AI Chat
with tab4:
    st.header("💬 Chat with AI Data Scientist")
    
    if gemini_key:
        query = st.text_area("Ask your question", 
                            placeholder="e.g., What insights can you provide about this data?",
                            height=100)
        
        if st.button("🤖 Get AI Insights", use_container_width=True, type="primary"):
            if query:
                with st.spinner("AI is thinking..."):
                    try:
                        model = genai.GenerativeModel('models/gemini-2.0-flash')
                        
                        # Build context
                        context = ""
                        if st.session_state.df is not None:
                            df = st.session_state.df
                            context = f"""
Dataset Info:
- Shape: {df.shape}
- Columns: {', '.join(df.columns)}
- Missing Data: {df.isnull().sum().sum()} values

Summary Statistics:
{df.describe().to_string()}
"""
                        
                        prompt = f"""You are an expert data scientist.

{context}

User Question: {query}

Provide detailed, professional insights."""
                        
                        response = model.generate_content(prompt)
                        
                        st.subheader("💡 AI Insights")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a question")
    else:
        st.warning("⚠️ Please enter Gemini API key in sidebar")

# Tab 5: Reports
with tab5:
    st.header("📄 Generate Reports")
    
    if st.session_state.df is not None:
        df = st.session_state.df
        
        st.info(f"📊 **Current Dataset:** {st.session_state.selected_dataset or 'Uploaded File'} | "
                f"{df.shape[0]} rows × {df.shape[1]} columns")
        
        st.subheader("📊 Report Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📄 Comprehensive PDF Report")
            st.write("Complete analysis with all statistics, visualizations & insights")
            if st.button("📊 Generate Comprehensive PDF", use_container_width=True, type="primary"):
                with st.spinner("🔄 Generating comprehensive PDF report... This may take a moment"):
                    try:
                        from modules.pdf_report_generator import ComprehensivePDFReport
                        
                        # Generate comprehensive PDF
                        pdf_gen = ComprehensivePDFReport(df, st.session_state.selected_dataset or "Dataset")
                        pdf_bytes = pdf_gen.generate_report()
                        
                        # Success message
                        st.success("✅ Comprehensive PDF Report Generated Successfully!")
                        st.info("📊 Report includes: Dataset Overview, Data Quality, Missing Values, Statistics, Correlations, Statistical Tests, Outlier Detection & Recommendations")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Comprehensive PDF Report",
                            data=pdf_bytes,
                            file_name=f"comprehensive_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error generating PDF: {str(e)}")
                        st.info("💡 Tip: Make sure all required packages are installed")
        
        with col2:
            st.markdown("### 📝 Markdown Report")
            st.write("Text-based report for documentation")
            if st.button("📝 Generate Markdown", use_container_width=True):
                df = st.session_state.df
                
                report = f"""# Data Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Overview
- Rows: {df.shape[0]}
- Columns: {df.shape[1]}
- Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB

## Summary Statistics
{df.describe().to_markdown()}

## Missing Data
{df.isnull().sum().to_frame('Missing').to_markdown()}

## Column Types
{df.dtypes.to_frame('Type').to_markdown()}
"""
                
                st.download_button(
                    "📥 Download Report",
                    report,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
                
                st.code(report, language='markdown')
        
        with col3:
            st.markdown("### 🐍 Python Code")
            st.write("Reproducible analysis code")
            if st.button("📓 Generate Code", use_container_width=True):
                code = f"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('your_data.csv')

# Basic info
print(df.info())
print(df.describe())

# Missing data
print(df.isnull().sum())

# Correlations
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# Distributions
df.hist(bins=30, figsize=(15, 10))
plt.tight_layout()
plt.show()
"""
                
                st.download_button(
                    "📥 Download Code",
                    code,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                    mime="text/x-python"
                )
                
                st.code(code, language='python')
    else:
        st.info("Load a dataset to generate reports")

# Tab 6: Advanced Statistics
with tab6:
    st.header("📈 Advanced Statistical Analysis")
    
    if st.session_state.df is not None:
        from modules.statistical_analysis import StatisticalAnalyzer
        
        df = st.session_state.df
        analyzer = StatisticalAnalyzer(df)
        
        stat_col1, stat_col2 = st.columns(2)
        
        with stat_col1:
            st.subheader("📊 Normality Tests")
            if st.button("Run Normality Tests"):
                results = analyzer.normality_tests()
                st.dataframe(pd.DataFrame(results).T)
        
        with stat_col2:
            st.subheader("📉 Distribution Analysis")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            selected_col = st.selectbox("Select column", numeric_cols, key="dist_col")
            if st.button("Analyze Distribution"):
                fig = analyzer.distribution_analysis(selected_col)
                st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🔗 Correlation Analysis")
        if st.button("Generate Correlation Matrix"):
            fig, corr_matrix = analyzer.correlation_analysis()
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(corr_matrix)
        
        st.subheader("📋 Descriptive Statistics")
        st.dataframe(analyzer.descriptive_stats())
    else:
        st.info("Load a dataset first")

# Tab 7: 3D Visualization
with tab7:
    st.header("🎨 3D Visualization")
    
    if st.session_state.df is not None:
        from modules.visualization_3d import Visualizer3D
        
        df = st.session_state.df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 3:
            viz_3d = Visualizer3D(df)
            
            viz_type = st.selectbox("Select visualization type", [
                "3D Scatter Plot",
                "3D Surface Plot",
                "3D PCA",
                "3D Bubble Chart"
            ])
            
            if viz_type == "3D Scatter Plot":
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_col = st.selectbox("X-axis", numeric_cols, key="3d_x")
                with col2:
                    y_col = st.selectbox("Y-axis", numeric_cols, key="3d_y")
                with col3:
                    z_col = st.selectbox("Z-axis", numeric_cols, key="3d_z")
                
                if st.button("Generate 3D Scatter"):
                    fig = viz_3d.scatter_3d(x_col, y_col, z_col)
                    st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "3D Surface Plot":
                col1, col2, col3 = st.columns(3)
                with col1:
                    x_col = st.selectbox("X-axis", numeric_cols, key="surf_x")
                with col2:
                    y_col = st.selectbox("Y-axis", numeric_cols, key="surf_y")
                with col3:
                    z_col = st.selectbox("Z-axis (values)", numeric_cols, key="surf_z")
                
                if st.button("Generate Surface Plot"):
                    fig = viz_3d.surface_plot(x_col, y_col, z_col)
                    st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "3D PCA":
                if st.button("Generate 3D PCA"):
                    fig, variance = viz_3d.pca_3d()
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        st.write("Explained Variance Ratio:", variance)
            
            elif viz_type == "3D Bubble Chart":
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    x_col = st.selectbox("X-axis", numeric_cols, key="bubble_x")
                with col2:
                    y_col = st.selectbox("Y-axis", numeric_cols, key="bubble_y")
                with col3:
                    z_col = st.selectbox("Z-axis", numeric_cols, key="bubble_z")
                with col4:
                    size_col = st.selectbox("Size", numeric_cols, key="bubble_size")
                
                if st.button("Generate Bubble Chart"):
                    fig = viz_3d.bubble_3d(x_col, y_col, z_col, size_col)
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 3 numeric columns for 3D visualization")
    else:
        st.info("Load a dataset first")

# Tab 8: Data Processing
with tab8:
    st.header("🧹 Advanced Data Processing")
    
    if st.session_state.df is not None:
        from modules.data_processing import DataProcessor
        
        df = st.session_state.df
        processor = DataProcessor(df)
        
        process_type = st.selectbox("Select processing task", [
            "Missing Value Analysis",
            "Handle Duplicates",
            "Encode Categorical",
            "Scale Features",
            "Handle Outliers",
            "Balance Dataset",
            "Data Quality Score"
        ])
        
        if process_type == "Missing Value Analysis":
            st.subheader("Missing Values")
            missing_df = processor.missing_value_analysis()
            if len(missing_df) > 0:
                st.dataframe(missing_df)
            else:
                st.success("✅ No missing values found!")
        
        elif process_type == "Handle Duplicates":
            duplicates = df.duplicated().sum()
            st.write(f"Found {duplicates} duplicate rows")
            if st.button("Remove Duplicates"):
                df_clean, count = processor.handle_duplicates()
                st.session_state.df = df_clean
                st.success(f"✅ Removed {count} duplicates")
        
        elif process_type == "Encode Categorical":
            cat_cols = df.select_dtypes(include=['object']).columns.tolist()
            if cat_cols:
                selected_cols = st.multiselect("Select columns to encode", cat_cols)
                method = st.selectbox("Encoding method", ["label", "onehot"])
                if st.button("Encode"):
                    df_encoded = processor.encode_categorical(selected_cols, method)
                    st.session_state.df = df_encoded
                    st.success("✅ Encoding complete")
            else:
                st.info("No categorical columns found")
        
        elif process_type == "Scale Features":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            selected_cols = st.multiselect("Select columns to scale", numeric_cols)
            method = st.selectbox("Scaling method", ["standard", "minmax"])
            if st.button("Scale"):
                df_scaled = processor.scale_features(selected_cols, method)
                st.session_state.df = df_scaled
                st.success("✅ Scaling complete")
        
        elif process_type == "Handle Outliers":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            selected_cols = st.multiselect("Select columns", numeric_cols)
            method = st.selectbox("Method", ["iqr", "zscore"])
            threshold = st.slider("Threshold", 1.0, 5.0, 1.5)
            if st.button("Handle Outliers"):
                df_clean, count = processor.handle_outliers(selected_cols, method, threshold)
                st.session_state.df = df_clean
                st.success(f"✅ Handled {count} outliers")
        
        elif process_type == "Balance Dataset":
            target_col = st.selectbox("Target column", df.columns)
            method = st.selectbox("Method", ["smote", "undersample"])
            if st.button("Balance"):
                result = processor.balance_dataset(target_col, method)
                if isinstance(result, tuple):
                    df_balanced, error_msg = result
                    st.error(f"⚠️ {error_msg}")
                else:
                    st.session_state.df = result
                    st.success("✅ Dataset balanced")
        
        elif process_type == "Data Quality Score":
            score = processor.get_data_quality_score()
            st.metric("Data Quality Score", f"{score:.2f}%")
    else:
        st.info("Load a dataset first")

# Tab 9: Anomaly Detection
with tab9:
    st.header("🎯 Anomaly Detection")
    
    if st.session_state.df is not None:
        from modules.anomaly_detection import AnomalyDetector
        
        df = st.session_state.df
        detector = AnomalyDetector(df)
        
        anomaly_type = st.selectbox("Detection method", [
            "Isolation Forest",
            "Statistical (Z-score)",
            "Statistical (IQR)"
        ])
        
        if anomaly_type == "Isolation Forest":
            contamination = st.slider("Contamination rate", 0.01, 0.5, 0.1)
            if st.button("Detect Anomalies"):
                df_anomaly, anomalies = detector.isolation_forest(contamination)
                st.session_state.df = df_anomaly
                
                summary = detector.get_anomaly_summary()
                st.dataframe(summary)
                
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) >= 2:
                    col1, col2 = st.columns(2)
                    with col1:
                        x_col = st.selectbox("X-axis", numeric_cols, key="anom_x")
                    with col2:
                        y_col = st.selectbox("Y-axis", numeric_cols, key="anom_y")
                    
                    fig = detector.visualize_anomalies(x_col, y_col)
                    st.plotly_chart(fig, use_container_width=True)
        
        elif anomaly_type == "Statistical (Z-score)":
            threshold = st.slider("Z-score threshold", 1.0, 5.0, 3.0)
            if st.button("Detect Anomalies"):
                df_anomaly, anomalies = detector.statistical_anomalies('zscore', threshold)
                st.session_state.df = df_anomaly
                
                summary = detector.get_anomaly_summary()
                st.dataframe(summary)
        
        elif anomaly_type == "Statistical (IQR)":
            if st.button("Detect Anomalies"):
                df_anomaly, anomalies = detector.statistical_anomalies('iqr')
                st.session_state.df = df_anomaly
                
                summary = detector.get_anomaly_summary()
                st.dataframe(summary)
    else:
        st.info("Load a dataset first")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p>🤖 AI Data Science Research Assistant | Powered by Gemini AI</p>
    <p>Built with Streamlit ❤️</p>
</div>
""", unsafe_allow_html=True)
