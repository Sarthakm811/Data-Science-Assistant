# LangChain Integration Guide

## Overview

The DS Research Agent now uses **LangChain** for sophisticated multi-tool orchestration, connecting Gemini + Kaggle + execution tools with ReAct reasoning.

## Architecture

```
User Query → LangChain Agent (ReAct)
              ↓
         Gemini (via LangChain)
              ↓
    Tool Selection & Execution
    - search_kaggle_datasets
    - get_dataset_info
    - execute_python_code
    - generate_analysis_plan
              ↓
         Final Answer
```

## Endpoints

### Standard Query (Direct Gemini)
```http
POST /api/v1/query
```

### LangChain Query (Multi-tool reasoning)
```http
POST /api/v1/query/langchain
```

## Example Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/query/langchain",
    json={
        "session_id": "your-session-id",
        "query": "Find housing datasets and show price distribution",
        "dataset_id": None
    }
)

print(response.json())
```

## Benefits of LangChain

1. **Multi-step reasoning**: Agent can chain multiple tools
2. **Self-correction**: ReAct pattern allows reflection
3. **Tool selection**: Automatically picks right tools
4. **Memory**: Maintains conversation context
5. **Extensibility**: Easy to add new tools

## Adding Custom Tools

```python
from langchain.tools import Tool

new_tool = Tool(
    name="your_tool_name",
    func=your_function,
    description="Clear description for LLM"
)

agent.tools.append(new_tool)
```

## Database Logging

All LangChain queries are logged to PostgreSQL:
- Query text
- Execution time
- Intermediate steps
- Final results

Query the logs:
```sql
SELECT * FROM queries 
WHERE created_at > NOW() - INTERVAL '1 day'
ORDER BY execution_time DESC;
```
