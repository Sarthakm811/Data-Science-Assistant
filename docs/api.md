# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### Health Check

```http
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Create Session

```http
POST /api/v1/sessions
```

Request:
```json
{
  "user_id": "optional-user-id"
}
```

Response:
```json
{
  "session_id": "uuid",
  "created_at": "2024-01-01T00:00:00",
  "last_activity": "2024-01-01T00:00:00"
}
```

### Submit Query

```http
POST /api/v1/query
```

Request:
```json
{
  "session_id": "uuid",
  "query": "Show me summary statistics",
  "dataset_id": "username/dataset-name"
}
```

Response:
```json
{
  "job_id": "uuid",
  "status": "completed",
  "plan": "Analysis plan text",
  "code": "Generated Python code",
  "results": {
    "key": "value"
  },
  "artifacts": ["/outputs/chart.png"],
  "explanation": "Natural language explanation"
}
```

### Search Datasets

```http
GET /api/v1/datasets/search?q=housing&page=1
```

Response:
```json
{
  "results": [
    {
      "id": "username/dataset",
      "title": "Dataset Title",
      "size": 1024000,
      "url": "https://kaggle.com/..."
    }
  ]
}
```

### Get Dataset Info

```http
GET /api/v1/datasets/{dataset_id}
```

Response:
```json
{
  "id": "username/dataset",
  "title": "Dataset Title",
  "description": "Description",
  "columns": ["col1", "col2"]
}
```

### Get Session History

```http
GET /api/v1/sessions/{session_id}/history
```

Response:
```json
{
  "history": [
    {
      "query": "User query",
      "response": "Agent response",
      "job_id": "uuid"
    }
  ]
}
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

Error format:
```json
{
  "detail": "Error message"
}
```

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per user

## Authentication

Currently open for development. Production deployment should use:
- OAuth 2.0 (Google)
- JWT tokens
- API keys for programmatic access
