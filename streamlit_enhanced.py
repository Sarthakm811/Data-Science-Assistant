import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import sys
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.abspath('.'))

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
if 'df' not in st.session_state:
    st.session_state.df = None
if 'gemini_key' not in st.session_state:
    st.session_state.gemini_key = ''
if 'kaggle_username' not in st.session_state:
    st.session_state.kaggle_username = ''
if 'kaggle_key' not in st.session_state:
    st.session_state.kaggle_key = ''

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("🔐 **Setup Required:** Enter your API credentials below")
    
    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Get from https://makersuite.google.com/app/apikey",
        placeholder="Enter your Gemini API key"
    )
    
    kaggle_username = st.text_input(
        "Kaggle Username",
        help="Get from https://www.kaggle.com/settings/account",
        placeholder="Enter your Kaggle username"
    )
    
    kaggle_key = st.text_input(
        "Kaggle API Key",
        type="password",
        help="Get from https://www.kaggle.com/settings/account",
        placeholder="Enter your Kaggle API key"
    )
    
    if st.button("Save Credentials"):
        st.session_state.gemini_key = gemini_key
        st.session_state.kaggle_username = kaggle_username
        st.session_state.kaggle_key = kaggle_key
        st.success("✅ Credentials saved for this session")
    
    st.markdown("---")
    st.caption("🔒 Your credentials are stored only in this session and never saved to disk")

# Main content
st.markdown('<h1 class="main-header">🤖 AI Data Science Research Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Your Personal AI Data Scientist</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Dataset Search",
    "📊 Auto EDA",
    "🤖 Auto ML",
    "💬 AI Chat",
    "📄 Reports",
    "🧹 Data Processing"
])

# Tab 1: Dataset Search
with tab1:
    st.header("🔍 Dataset Search")
    st.info("Search and download datasets from Kaggle")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search for datasets", placeholder="e.g., titanic, iris, housing")
    with col2:
        search_btn = st.button("Search", key="search_btn")
    
    if search_btn:
        if not search_query:
            st.warning("Please enter a search query")
        elif not st.session_state.kaggle_username or not st.session_state.kaggle_key:
            st.warning("Please configure Kaggle credentials in the sidebar")
        else:
            st.info("🔄 Searching for datasets... (Feature coming soon)")

# Tab 2: Auto EDA
with tab2:
    st.header("📊 Auto EDA")
    st.info("Automatic Exploratory Data Analysis")
    
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            
            st.success(f"✅ Dataset Loaded")
            st.write(f"**Name:** {uploaded_file.name}")
            st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
            
            if st.button("Run EDA Analysis"):
                st.info("🔄 Running analysis...")
                
                # Basic statistics
                st.subheader("📈 Summary Statistics")
                st.dataframe(df.describe())
                
                # Missing data
                st.subheader("❌ Missing Data")
                missing = df.isnull().sum()
                if missing.sum() > 0:
                    st.bar_chart(missing[missing > 0])
                else:
                    st.success("✅ No missing data found!")
                
                # Data types
                st.subheader("📋 Data Types")
                st.write(df.dtypes)
                
                st.success("✅ Analysis complete!")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

# Tab 3: Auto ML
with tab3:
    st.header("🤖 Auto ML")
    st.info("Automatic Machine Learning Model Training")
    
    if st.session_state.df is not None:
        st.write(f"Current Dataset: {st.session_state.df.shape[0]} rows × {st.session_state.df.shape[1]} columns")
        
        numeric_cols = st.session_state.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            target = st.selectbox("Select target column", numeric_cols)
            
            if st.button("Train Models"):
                st.info("🔄 Training models... (Feature coming soon)")
        else:
            st.warning("No numeric columns found in dataset")
    else:
        st.info("Upload a dataset in the Auto EDA tab first")

# Tab 4: AI Chat
with tab4:
    st.header("💬 AI Chat")
    st.info("Ask questions about your data")
    
    if not st.session_state.gemini_key:
        st.warning("Please configure Gemini API key in the sidebar")
    else:
        st.success("✅ Gemini API configured")
        
        user_input = st.text_input("Ask a question about your data")
        
        if user_input:
            st.info("🔄 Processing... (Feature coming soon)")

# Tab 5: Reports
with tab5:
    st.header("📄 Reports")
    st.info("Generate professional reports")
    
    if st.session_state.df is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Generate PDF Report"):
                st.info("🔄 Generating PDF... (Feature coming soon)")
        
        with col2:
            if st.button("📝 Generate Markdown Report"):
                st.info("🔄 Generating Markdown... (Feature coming soon)")
    else:
        st.info("Upload a dataset in the Auto EDA tab first")

# Tab 6: Data Processing
with tab6:
    st.header("🧹 Data Processing")
    st.info("Data cleaning and preprocessing tools")
    
    if st.session_state.df is not None:
        st.subheader("Dataset Preview")
        st.dataframe(st.session_state.df.head(10))
        
        st.subheader("Data Info")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", st.session_state.df.shape[0])
        with col2:
            st.metric("Columns", st.session_state.df.shape[1])
        with col3:
            st.metric("Memory", f"{st.session_state.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    else:
        st.info("Upload a dataset in the Auto EDA tab first")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🤖 AI Data Science Research Assistant | Powered by Gemini AI</p>
    <p>Built with Streamlit ❤️</p>
</div>
""", unsafe_allow_html=True)
