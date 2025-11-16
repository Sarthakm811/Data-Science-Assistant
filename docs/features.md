# Feature Overview

## Core Features

### 1. Natural Language Queries
Ask questions in plain English:
- "Show me summary statistics"
- "What are the top correlated features?"
- "Build a baseline model"

### 2. Dual Query Modes

#### Standard Mode (Fast)
- Direct Gemini code generation
- Single-step execution
- Best for simple queries
- Endpoint: `POST /api/v1/query`

#### LangChain Mode (Smart)
- Multi-tool reasoning with ReAct pattern
- Can chain multiple operations
- Self-correcting
- Best for complex workflows
- Endpoint: `POST /api/v1/query/langchain`

### 3. Kaggle Integration
- Search 50,000+ datasets
- Automatic dataset download
- Metadata caching
- Popular dataset recommendations

### 4. Code Generation & Execution
- Gemini generates Python code
- Sandboxed execution environment
- Support for: Pandas, NumPy, Scikit-learn, Matplotlib, Plotly
- Automatic artifact collection (charts, CSVs)

### 5. Session Management
- Persistent sessions with Redis
- Context retention across queries
- Query history
- Current dataset tracking

### 6. Database Storage

#### PostgreSQL (Default)
- Query logs with execution time
- Dataset metadata cache
- API request logs
- Session information

#### Firebase (Alternative)
- NoSQL document storage
- Real-time updates
- Easy scaling

### 7. Security Features
- Sandboxed code execution
- No network access from executor
- Resource limits (CPU, memory, time)
- Input validation
- PII filtering

## Advanced Features

### LangChain Tools

1. **search_kaggle_datasets**
   - Search Kaggle by keyword
   - Returns top matches

2. **get_dataset_info**
   - Fetch dataset metadata
   - Column information
   - Size and description

3. **execute_python_code**
   - Run generated code safely
   - Collect outputs and artifacts

4. **generate_analysis_plan**
   - Create step-by-step plans
   - Break down complex queries

### Multi-Step Workflows

Example: "Find housing data and build a model"

1. Agent searches Kaggle
2. Selects best dataset
3. Downloads and loads data
4. Performs EDA
5. Trains baseline model
6. Generates explanation

### Observability

- Structured logging (JSON)
- OpenTelemetry traces
- Prometheus metrics
- Query execution tracking
- Error monitoring

## Coming Soon

- [ ] SHAP/LIME explanations
- [ ] Notebook export to Kaggle
- [ ] Vector DB for long-term memory
- [ ] Multi-agent collaboration
- [ ] Real-time streaming results
- [ ] Custom tool registration
- [ ] Role-based access control
- [ ] Cost tracking per query

## API Capabilities

### REST Endpoints

```
POST   /api/v1/sessions              Create session
GET    /api/v1/sessions/{id}/history Get history
POST   /api/v1/query                 Standard query
POST   /api/v1/query/langchain       LangChain query
GET    /api/v1/datasets/search       Search datasets
GET    /api/v1/datasets/{id}         Get dataset info
GET    /health                       Health check
```

### Response Format

```json
{
  "job_id": "uuid",
  "status": "completed",
  "plan": "Analysis plan text",
  "code": "Generated Python code",
  "results": {"key": "value"},
  "artifacts": ["/outputs/chart.png"],
  "explanation": "Natural language summary"
}
```

## Performance

- Average query time: 3-8 seconds
- Code execution timeout: 45 seconds
- Session TTL: 1 hour
- Database query caching
- Horizontal scaling ready

## Extensibility

### Add Custom Tools

```python
from langchain.tools import Tool

custom_tool = Tool(
    name="my_tool",
    func=my_function,
    description="Tool description for LLM"
)

agent.tools.append(custom_tool)
```

### Add New Endpoints

```python
@router.post("/custom")
async def custom_endpoint():
    # Your logic
    pass
```

### Integrate New Data Sources

Extend `KaggleTool` pattern for:
- Google BigQuery
- AWS S3
- Hugging Face datasets
- Custom APIs
