# 🚀 Complete Setup & Troubleshooting Guide

**Last Updated:** November 24, 2025  
**Version:** 3.0 (Enhanced)

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Setup](#advanced-setup)
8. [Performance Optimization](#performance-optimization)

---

## ⚡ Quick Start

**For Windows Users:**
```bash
# 1. Just double-click START.bat
# 2. Your browser will open automatically
# 3. Enter your API keys in the sidebar
# Done! ✅
```

**For Mac/Linux Users:**
```bash
python -m pip install -r requirements-streamlit.txt
streamlit run streamlit_enhanced.py
```

---

## 📦 Prerequisites

### Required
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **pip** - Usually included with Python
- **At least 2GB free disk space**
- **At least 4GB RAM** (8GB recommended)
- **Internet connection** (for API calls and dataset downloads)

### Required API Keys (Free)
1. **Gemini API Key** - Free tier available
2. **Kaggle Account** - Free account required

---

## 🔐 Step 1: Get API Credentials

### 1.1 Gemini API Key (5 minutes)

```
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Keep it safe - you'll need it later
```

**Free tier:**
- ✅ 50 requests per minute
- ✅ 1,500 requests per day
- ✅ 0 cost

### 1.2 Kaggle Credentials (5 minutes)

```
1. Go to: https://www.kaggle.com/settings/account
2. Scroll down to "API" section
3. Click "Create New Token"
4. A file "kaggle.json" will download
5. Open kaggle.json with a text editor
6. You'll see "username" and "key"
7. Keep these safe - you'll need them later
```

**Free tier:**
- ✅ Access to 50,000+ datasets
- ✅ 0 cost
- ✅ No rate limits for basic use

---

## 💻 Step 2: Install Application

### Option A: Windows (Easiest)

**Using Command Prompt:**
```batch
# 1. Download the project
git clone https://github.com/Sarthakm811/Data-Science-Assistant.git
cd Data-Science-Assistant

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements-streamlit.txt

# 4. Setup environment
copy .env.template .env
# Now edit .env and add your API keys
```

**Or just click START.bat:**
```
START.bat automatically does steps 1-4!
```

### Option B: Mac/Linux

**Using Terminal:**
```bash
# 1. Download the project
git clone https://github.com/Sarthakm811/Data-Science-Assistant.git
cd Data-Science-Assistant

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements-streamlit.txt

# 4. Setup environment
cp .env.template .env
# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

---

## ⚙️ Step 3: Configuration

### 3.1 Edit .env File

```bash
# Open .env with your text editor
# Windows: notepad .env
# Mac: nano .env
# Linux: nano .env
```

**Edit these fields:**
```env
GEMINI_API_KEY=paste_your_gemini_key_here
KAGGLE_USERNAME=paste_your_username
KAGGLE_KEY=paste_your_key_here
```

**Example (after editing):**
```env
GEMINI_API_KEY=AIzaSyDxxx...xxxxx
KAGGLE_USERNAME=john_doe
KAGGLE_KEY=xxxxx...xxxxx
```

### 3.2 Verify Configuration

```bash
# Test if environment is loaded correctly
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ Configuration loaded')"
```

---

## 🎯 Step 4: Run Application

### Option A: Using START.bat (Windows Only)
```
Just double-click: START.bat
Your browser will open automatically! 🎉
```

### Option B: Using Terminal

```bash
# Make sure venv is activated first:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Then run:
streamlit run streamlit_enhanced.py

# You'll see:
# Local URL: http://localhost:8501
# Network URL: http://192.168.x.x:8501

# Press Ctrl+C to stop
```

### Option C: Using Docker

```bash
# Build image
docker build -t ds-assistant:latest .

# Run container
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your_key \
  -e KAGGLE_USERNAME=your_username \
  -e KAGGLE_KEY=your_key \
  ds-assistant:latest

# Access at: http://localhost:8501
```

---

## 📱 Using the Application

### First-Time Setup

1. **Enter API Keys in Sidebar**
   - Scroll to the sidebar (left side)
   - Enter your Gemini API Key
   - Enter your Kaggle Username and Key
   - ✅ These are stored only in your browser session

2. **Upload Your Dataset**
   - Go to "📁 Upload Dataset" in sidebar
   - Choose a CSV file (or use "Dataset Search" to find one)
   - Wait for it to load

3. **Run Auto EDA**
   - Click "📊 Auto EDA" tab
   - Click "Run Full EDA" button
   - Wait 30-60 seconds for analysis
   - 🎉 You'll see tons of insights!

4. **Train ML Models**
   - Click "🤖 Auto ML" tab
   - Select target column (what you want to predict)
   - Click "Train Models"
   - Compare model performance

5. **Get AI Insights**
   - Click "💬 AI Chat" tab
   - Ask questions about your data
   - Get professional insights!

6. **Download Report**
   - Click "📄 Reports" tab
   - Click "Generate Report"
   - Download as Markdown or PDF

---

## ⚠️ Troubleshooting

### Problem 1: "Module not found" Error

**Error Message:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
# Make sure venv is activated:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Then reinstall:
pip install -r requirements-streamlit.txt

# Verify:
python -c "import streamlit; print('✅ Streamlit installed')"
```

---

### Problem 2: "API Key Invalid" Error

**Error Message:**
```
ValueError: Invalid API key
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Key not copied correctly | Copy again from API console, avoid spaces |
| Wrong API key | Check you're using Gemini, not other API |
| API key expired | Regenerate new key from console |
| Key in wrong format | Should be long alphanumeric string |

**Quick Test:**
```python
import google.generativeai as genai
genai.configure(api_key="your_key_here")
model = genai.GenerativeModel("models/gemini-2.0-flash")
response = model.generate_content("Say hello")
print(response.text)  # Should print "Hello"
```

---

### Problem 3: "Kaggle Authentication Failed"

**Error Message:**
```
OSError: Could not find kaggle.json
```

**Solutions:**

1. **Check .env file:**
   ```bash
   # Verify KAGGLE_USERNAME and KAGGLE_KEY are set
   cat .env  # Mac/Linux
   type .env  # Windows
   ```

2. **Check kaggle.json:**
   ```bash
   # Should exist at ~/.kaggle/kaggle.json
   # Windows: C:\Users\YourUsername\.kaggle\kaggle.json
   # Mac/Linux: ~/.kaggle/kaggle.json
   
   # If it doesn't exist:
   # 1. Go to https://www.kaggle.com/settings/account
   # 2. Click "Create New Token"
   # 3. Move the downloaded file to ~/.kaggle/
   ```

3. **Verify credentials:**
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   
   print(f"Username: {os.getenv('KAGGLE_USERNAME')}")
   print(f"Key: {os.getenv('KAGGLE_KEY')}")
   # Should print your credentials
   ```

---

### Problem 4: "File Encoding Error"

**Error Message:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Solutions:**

The app tries multiple encodings automatically. If it still fails:

1. **Try these encodings:**
   - UTF-8 (most common) ✅ Default
   - Latin-1
   - ISO-8859-1
   - Windows-1252
   - UTF-16

2. **Convert your file:**
   ```python
   import pandas as pd
   
   # Read with problematic encoding
   df = pd.read_csv('file.csv', encoding='latin-1')
   
   # Save with clean encoding
   df.to_csv('file_clean.csv', encoding='utf-8', index=False)
   ```

---

### Problem 5: "Out of Memory" or Slow Performance

**Error Message:**
```
MemoryError or application becomes unresponsive
```

**Solutions:**

1. **Check file size:**
   ```bash
   # Windows: Right-click file → Properties → Size
   # Mac/Linux: ls -lh filename.csv
   # Ideal: < 100 MB
   # Warning: 100-500 MB
   # Error: > 500 MB
   ```

2. **Reduce dataset:**
   ```python
   import pandas as pd
   
   df = pd.read_csv('large_file.csv')
   df_sample = df.sample(n=10000)  # Take 10k rows
   df_sample.to_csv('small_file.csv', index=False)
   ```

3. **Increase system resources:**
   ```bash
   # Docker: Add more memory
   docker run -m 4g streamlit_app:latest
   
   # Or use cloud deployment (Railway, Heroku, AWS)
   ```

---

### Problem 6: "Connection Timeout" or "Dataset Download Failed"

**Error Message:**
```
ConnectionError: Failed to download dataset
```

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Internet connection lost | Check connection and retry |
| Kaggle API rate limited | Wait 1 hour before retrying |
| Dataset not found | Check dataset name and try different one |
| Dataset size too large | Try smaller dataset first |

**Retry Logic:**
```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        # Your code here
        break
    except Exception as e:
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            print(f"Retrying in {wait_time}s...")
            time.sleep(wait_time)
        else:
            print(f"Failed after {max_retries} attempts")
            raise
```

---

### Problem 7: "Port Already in Use"

**Error Message:**
```
Address already in use: ('127.0.0.1', 8501)
```

**Solutions:**

```bash
# Option 1: Kill existing process
# Windows: taskkill /PID 12345
# Mac/Linux: kill -9 12345

# Option 2: Use different port
streamlit run streamlit_enhanced.py --server.port 8502

# Option 3: Check what's using port 8501
# Windows: netstat -ano | findstr :8501
# Mac/Linux: lsof -i :8501
```

---

### Problem 8: "Changes Not Reflecting"

**Error Message:**
```
Code changes not showing up in the app
```

**Solutions:**

1. **Streamlit resets on file save (normal behavior)**
   - Just wait, it will refresh automatically
   - You'll see "rerun" notification

2. **Hard refresh your browser:**
   - Press Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

3. **Restart Streamlit:**
   ```bash
   # Stop: Ctrl+C
   # Then: streamlit run streamlit_enhanced.py
   ```

4. **Clear cache:**
   ```bash
   streamlit cache clear
   streamlit run streamlit_enhanced.py
   ```

---

## 🚀 Advanced Setup

### Custom Python Environment

```bash
# Use specific Python version
python3.10 -m venv venv_py310

# Activate and install
source venv_py310/bin/activate
pip install -r requirements-streamlit.txt
```

### Development Mode

```bash
# Install development dependencies
pip install -r requirements-streamlit.txt
pip install pytest black flake8 pylint

# Run tests
pytest tests/

# Format code
black streamlit_enhanced.py

# Lint code
pylint streamlit_enhanced.py
```

### Deployment

**Railway (1-click deployment):**
```bash
# 1. Push code to GitHub
# 2. Go to https://railway.app
# 3. Click "New Project"
# 4. Select "Deploy from GitHub"
# 5. Add environment variables in Railway dashboard
# 6. Done! 🎉
```

**Heroku:**
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku config:set GEMINI_API_KEY=your_key
heroku open
```

**Docker Hub:**
```bash
docker build -t your-username/ds-assistant:latest .
docker push your-username/ds-assistant:latest
```

---

## ⚙️ Performance Optimization

### 1. Enable Caching

```python
import streamlit as st

@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)

@st.cache_resource
def get_ml_model():
    return load_ml_model()
```

### 2. Parallel Processing

```python
from multiprocessing import Pool

def process_large_dataset(df):
    with Pool() as p:
        results = p.map(process_chunk, chunks)
    return pd.concat(results)
```

### 3. Optimize Visualizations

```python
# Use plotly instead of matplotlib for interactivity
# Limit data points in scatter plots
# Pre-aggregate large datasets
# Use Streamlit columns for side-by-side display
```

### 4. Memory Management

```python
# Delete unused dataframes
del df_temp

# Use chunks for large files
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    process_chunk(chunk)

# Monitor memory
import tracemalloc
tracemalloc.start()
```

---

## 📊 Monitoring & Logs

### View Streamlit Logs

```bash
streamlit run streamlit_enhanced.py --logger.level=debug
```

### View Docker Logs

```bash
docker logs -f container_name
docker logs -f container_name --tail 100  # Last 100 lines
docker logs -f container_name --timestamps  # With timestamps
```

### Debug Mode

```python
# In streamlit_enhanced.py
DEBUG = True

if DEBUG:
    st.write("## 🔧 Debug Info")
    st.write(f"Dataframe shape: {st.session_state.df.shape}")
    st.write(f"Session state: {dict(st.session_state)}")
```

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] START.bat works (Windows) or terminal command works
- [ ] Streamlit app opens in browser
- [ ] Can enter API keys in sidebar
- [ ] Can upload CSV file successfully
- [ ] Can search and download Kaggle dataset
- [ ] Auto EDA runs without errors
- [ ] Auto ML trains models
- [ ] AI Chat generates responses
- [ ] Report generation works
- [ ] All features are fast and responsive

---

## 📞 Getting Help

### Resources

1. **Documentation:**
   - README.md - Project overview
   - DEBUG_AND_FIXES.md - Technical details
   - This file - Setup guide

2. **External Resources:**
   - [Streamlit Docs](https://docs.streamlit.io/)
   - [Gemini API Docs](https://ai.google.dev/)
   - [Kaggle API Docs](https://github.com/Kaggle/kaggle-api)

3. **Common Issues:**
   - Check "Troubleshooting" section above
   - Search GitHub issues
   - Check logs (see "Monitoring & Logs" above)

4. **Community Support:**
   - GitHub Discussions
   - Stack Overflow (tag: streamlit, gemini-api)
   - Kaggle Forums

---

## 🔄 Next Steps

1. ✅ **Setup Complete?** → Enjoy using the app! 🎉
2. 📚 **Want to Learn More?** → Read DEBUG_AND_FIXES.md
3. 🔧 **Want to Customize?** → Check out the code and modify
4. 🚀 **Ready to Deploy?** → See "Advanced Setup" section

---

**Need Help?** Check the troubleshooting section above, or create a GitHub issue!

**Last Updated:** November 24, 2025
