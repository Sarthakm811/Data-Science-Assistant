# Quick Start Guide

## Local Development

### 1. Clone Repository

```bash
git clone <repo-url>
cd ds-research-agent
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required keys:
- `GEMINI_API_KEY`: Get from [AI Studio](https://makersuite.google.com/app/apikey)
- `KAGGLE_USERNAME` & `KAGGLE_KEY`: Get from [Kaggle Account](https://www.kaggle.com/settings)

### 3. Start with Docker Compose

```bash
docker-compose up --build
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Try Your First Query

1. Open http://localhost:3000
2. Enter a dataset ID (e.g., `zillow/zecon`)
3. Ask: "Show me summary statistics for all numeric columns"
4. View the generated code and results

## Manual Setup (Without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Redis

```bash
docker run -d -p 6379:6379 redis:7-alpine
```

## Example Queries

### EDA
"Perform exploratory data analysis on this dataset"

### Correlation
"Show top 5 features correlated with the target variable"

### Visualization
"Create a scatter plot of price vs square footage"

### Modeling
"Build a baseline regression model and show feature importance"

## Next Steps

- Read [Architecture](./architecture.md)
- See [Deployment Guide](./deployment.md)
- Check [API Documentation](http://localhost:8000/docs)
