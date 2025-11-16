# 🔐 Setup Guide - API Credentials

This guide will help you set up the required API credentials for the AI Data Science Research Assistant.

## Why Do I Need API Keys?

- **Gemini API Key**: Powers the AI chat feature for intelligent data insights
- **Kaggle Credentials**: Enables searching and downloading datasets from Kaggle

## 📝 Step-by-Step Setup

### 1. Get Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Select a Google Cloud project (or create a new one)
5. Copy the generated API key
6. Paste it in the app sidebar under "Gemini API Key"

**Note:** Gemini API has a free tier with generous limits for testing.

### 2. Get Kaggle Credentials

1. Visit: https://www.kaggle.com/settings/account
2. Sign in or create a Kaggle account (it's free!)
3. Scroll down to the **"API"** section
4. Click **"Create New Token"**
5. A file named `kaggle.json` will be downloaded
6. Open the file - it contains your username and key:
   ```json
   {
     "username": "your_username",
     "key": "your_api_key_here"
   }
   ```
7. Copy the username and key
8. Paste them in the app sidebar

## 🔒 Security Best Practices

### ✅ DO:
- Keep your API keys private
- Never share your keys in screenshots or videos
- Use different keys for different projects
- Regenerate keys if you suspect they've been compromised

### ❌ DON'T:
- Commit API keys to Git repositories
- Share keys in public forums or chat
- Use the same key across multiple applications
- Store keys in plain text files

## 🛡️ How Your Keys Are Protected

- **Session Only**: Keys are stored only in your browser session
- **Not Saved**: Keys are never written to disk or database
- **Encrypted Input**: Password fields hide your keys as you type
- **Local Processing**: All processing happens on your machine

## 🔄 Alternative: Environment Variables (Advanced)

If you prefer, you can set environment variables instead:

### Windows:
```cmd
set GEMINI_API_KEY=your_key_here
set KAGGLE_USERNAME=your_username
set KAGGLE_KEY=your_kaggle_key
streamlit run streamlit_enhanced.py
```

### Linux/Mac:
```bash
export GEMINI_API_KEY=your_key_here
export KAGGLE_USERNAME=your_username
export KAGGLE_KEY=your_kaggle_key
streamlit run streamlit_enhanced.py
```

### Using .env file:
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your credentials:
   ```
   GEMINI_API_KEY=your_key_here
   KAGGLE_USERNAME=your_username
   KAGGLE_KEY=your_kaggle_key
   ```
3. Run the app normally

## ❓ Troubleshooting

### "Invalid API Key" Error
- Double-check you copied the entire key
- Make sure there are no extra spaces
- Try regenerating the key

### "Kaggle Authentication Failed"
- Verify both username and key are correct
- Check if your Kaggle account is verified
- Try creating a new API token

### "Rate Limit Exceeded"
- Gemini API: Wait a few minutes or upgrade to paid tier
- Kaggle API: You may have hit the hourly limit

## 📚 Additional Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Kaggle API Documentation](https://www.kaggle.com/docs/api)
- [Google Cloud Console](https://console.cloud.google.com/)

## 💡 Tips

1. **Test Your Keys**: After entering, try a simple operation to verify they work
2. **Free Tiers**: Both services offer generous free tiers for learning
3. **Backup Keys**: Save your keys in a secure password manager
4. **Monitor Usage**: Check your API usage dashboards regularly

## 🆘 Need Help?

If you're still having trouble:
1. Check the error message in the app
2. Review this guide again
3. Check the official documentation links above
4. Ensure you're using the latest version of the app

---

**Remember:** Your API keys are like passwords - keep them safe! 🔐
