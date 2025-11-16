# 🚀 Streamlit Setup Guide

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements-streamlit.txt
```

### Step 2: Configure API Keys
Edit `kaggle.json`:
```json
{
  "username": "your_kaggle_username",
  "key": "your_api_key"
}
```

Get Gemini API key from: https://ai.google.dev/

### Step 3: Run the App
```bash
# Enhanced version (Recommended!)
streamlit run streamlit_enhanced.py

# Or basic version
streamlit run streamlit_app.py
```

## 🎯 Access the App

Open your browser to: **http://localhost:8501**

## ✨ Features

### Enhanced Version (`streamlit_enhanced.py`)
- 🔍 **Dataset Search**: Search and download from Kaggle
- 📊 **Auto EDA**: Complete exploratory analysis with visualizations
- 🤖 **Auto ML**: Train and compare multiple models
- 💬 **AI Chat**: Ask questions and get insights
- 📄 **Reports**: Generate markdown reports and Python code

### Basic Version (`streamlit_app.py`)
- 💬 Chat interface
- 📊 Basic analysis
- 📚 Query history

## 📋 Configuration

### In the Sidebar
1. Enter your **Gemini API Key**
2. Enter your **Kaggle Username**
3. Enter your **Kaggle API Key**

### Upload Dataset
- Click "Upload CSV" in sidebar
- Or search Kaggle datasets

## 🎯 How to Use

### Option 1: Search Kaggle Dataset
1. Go to "🔍 Dataset Search" tab
2. Type search query (e.g., "titanic")
3. Click "🔎 Search"
4. Click "📥 Download & Load" on any dataset

### Option 2: Upload Your Data
1. Click "Upload CSV" in sidebar
2. Select your CSV file
3. Dataset loads automatically

### Run Auto EDA
1. Go to "📊 Auto EDA" tab
2. Click "🚀 Run Full EDA"
3. Get comprehensive analysis with:
   - Dataset overview
   - Summary statistics
   - Missing data analysis
   - Correlation heatmap
   - Distribution plots
   - Outlier detection

### Run Auto ML
1. Go to "🤖 Auto ML" tab
2. Select target variable
3. Choose task type (or auto-detect)
4. Click "🚀 Train Models"
5. Get model comparison and best model

### Chat with AI
1. Go to "💬 AI Chat" tab
2. Type your question
3. Click "🤖 Get AI Insights"
4. Get professional data science insights

### Generate Reports
1. Go to "📄 Reports" tab
2. Click "📝 Generate Markdown Report"
3. Or click "📓 Generate Python Code"
4. Download the generated files

## 📊 Example Workflow

```
1. Search "housing" dataset
   ↓
2. Download & Load
   ↓
3. Run Auto EDA
   ↓
4. Run Auto ML (target: price)
   ↓
5. Chat: "What factors affect price most?"
   ↓
6. Generate Report
   ↓
7. Download & Submit!
```

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements-streamlit.txt
```

### Kaggle API error
- Check credentials in sidebar
- Verify at kaggle.com/settings
- Ensure kaggle.json is in home directory

### Gemini API error
- Check API key is correct
- Verify at ai.google.dev
- Check API quota

### Port already in use
```bash
streamlit run streamlit_enhanced.py --server.port 8502
```

## 🎨 Customization

### Change Theme
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Change Port
```bash
streamlit run streamlit_enhanced.py --server.port 8502
```

### Enable Wide Mode by Default
Already enabled in the app!

## 🚀 Deployment

### Streamlit Cloud (Free!)
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Add secrets (API keys)
5. Deploy!

### Heroku
```bash
# Create Procfile
echo "web: streamlit run streamlit_enhanced.py --server.port $PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-streamlit.txt .
RUN pip install -r requirements-streamlit.txt

COPY streamlit_enhanced.py .
COPY kaggle.json .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_enhanced.py"]
```

## 📝 Tips & Tricks

### Faster Loading
- Use smaller datasets for testing
- Cache data with `@st.cache_data`

### Better Performance
- Limit visualizations for large datasets
- Use sampling for EDA

### Save Results
- Download reports regularly
- Export visualizations as PNG

## 🎓 Example Queries for AI Chat

- "What are the key insights from this data?"
- "Which features are most important?"
- "What patterns do you see?"
- "Generate hypotheses for research"
- "Recommend next steps for analysis"

## 📚 Additional Resources

- Streamlit Docs: https://docs.streamlit.io
- Gemini API: https://ai.google.dev
- Kaggle API: https://www.kaggle.com/docs/api

## ✅ Quick Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Gemini API key obtained
- [ ] Kaggle credentials configured
- [ ] App running on localhost:8501
- [ ] First analysis completed

## 🎉 You're Ready!

Run the enhanced version:
```bash
streamlit run streamlit_enhanced.py
```

Then open: http://localhost:8501

Start analyzing data with AI! 🚀
