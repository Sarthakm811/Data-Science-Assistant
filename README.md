# 🤖 AI Data Science Research Assistant

**Your Personal AI Data Scientist** - Built with Streamlit + Gemini AI

Analyze datasets, build ML models, and get professional insights with just a few clicks!

## 🔐 Prerequisites

Before running the app, you need to obtain API credentials:

### 1. **Gemini API Key** (Required for AI Chat)
- Visit: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy your API key

### 2. **Kaggle Credentials** (Required for Dataset Search)
- Visit: https://www.kaggle.com/settings/account
- Scroll to "API" section
- Click "Create New Token"
- Download `kaggle.json` file
- Copy username and key from the file

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements-streamlit.txt
```

### 2. Run the Application
```bash
streamlit run streamlit_enhanced.py
```
Or double-click: **START.bat** (Windows)

### 3. Open in Browser
Navigate to: **http://localhost:8501**

### 4. Configure API Keys
In the sidebar, enter:
- **Gemini API Key** - For AI-powered insights
- **Kaggle Username** - For dataset search
- **Kaggle API Key** - For dataset downloads

> 💡 **Note:** Your credentials are only stored in your browser session and are never saved to disk.

## ✨ Features

### 🔍 Dataset Search
- Search Kaggle datasets
- One-click download
- Upload your own CSV

### 📊 Auto EDA
- Summary statistics
- Missing data analysis
- Correlation heatmap
- Distribution plots
- Outlier detection
- 5+ visualizations

### 🤖 Auto ML
- Train multiple models
- Compare performance
- Best model selection
- Accuracy metrics

### 💬 AI Chat
- Ask questions in plain English
- Get professional insights
- Powered by Gemini AI

### 📄 Reports
- Generate markdown reports
- Export Python code
- Downloadable files

## 💡 Example Usage

1. **Search "titanic"** → Download dataset
2. **Run Auto EDA** → Get comprehensive analysis
3. **Run Auto ML** → Compare models
4. **Chat with AI** → Get insights
5. **Generate Report** → Download

## 🎓 Perfect For

✅ College assignments
✅ Research papers
✅ Interview prep
✅ Portfolio projects
✅ Quick data analysis

## 📚 Documentation

- **[README_FIRST.md](README_FIRST.md)** - Quick welcome
- **[00_START_HERE.md](00_START_HERE.md)** - Getting started
- **[STREAMLIT_SETUP.md](STREAMLIT_SETUP.md)** - Complete setup
- **[STREAMLIT_FEATURES.md](STREAMLIT_FEATURES.md)** - All features
- **[FEATURES.md](FEATURES.md)** - Detailed features

## 🐛 Troubleshooting

**Installation issues:**
```bash
pip install --upgrade pip
pip install -r requirements-streamlit.txt
```

**Port in use:**
```bash
streamlit run streamlit_enhanced.py --server.port 8502
```

**API errors:**
- Check Gemini key at ai.google.dev
- Check Kaggle credentials at kaggle.com/settings

## 🚀 Deployment

### Streamlit Cloud (Free!)
1. Push to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Add API keys as secrets
5. Deploy!

## 🔧 Tech Stack

- Streamlit - Web framework
- Gemini AI - AI insights
- Kaggle API - Dataset access
- Pandas & NumPy - Data processing
- Scikit-learn - Machine learning
- Matplotlib & Seaborn - Visualizations

## 📝 License

MIT License

---

**Start now:** `streamlit run streamlit_enhanced.py`

**Or:** Double-click `START.bat`

**Then:** Open http://localhost:8501

🚀 **Happy analyzing!**
