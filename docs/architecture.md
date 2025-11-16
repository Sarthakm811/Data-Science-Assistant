# Architecture Overview

## System Components

### Frontend (React/Next.js)
- User interface for queries and visualizations
- Real-time result display
- Session management
- Dataset browsing

### API Backend (FastAPI)
- REST API endpoints
- Session orchestration
- Gemini integration
- Tool coordination
- Memory management

### Executor (Python Sandbox)
- Isolated code execution
- Resource limits (CPU, memory, time)
- Artifact generation
- Security sandboxing

### Data Layer
- Redis: Session state, job queue
- Vector DB: Long-term memory, embeddings
- Object Storage: Artifacts, notebooks

## Data Flow

```
User Query → Frontend → Backend API
                          ↓
                    Gemini ADK (plan + code)
                          ↓
                    Executor (run code)
                          ↓
                    Results + Artifacts
                          ↓
                    Frontend Display
```

## Security Model

1. Code Sandboxing
   - No network access
   - Limited filesystem
   - Resource caps
   - Timeout enforcement

2. API Security
   - Rate limiting
   - Authentication (OAuth)
   - Input validation
   - Secret management

3. Data Privacy
   - PII filtering
   - Encrypted storage
   - Access controls
   - Audit logging

## Scalability

- Horizontal scaling via Kubernetes HPA
- Stateless backend design
- Redis for distributed sessions
- Async execution queue
- CDN for static assets

## Observability

- Structured logging (JSON)
- OpenTelemetry traces
- Prometheus metrics
- Grafana dashboards
- Error tracking (Sentry)
