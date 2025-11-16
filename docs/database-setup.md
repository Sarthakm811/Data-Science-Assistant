# Database Setup Guide

## PostgreSQL (Recommended)

### Local Development with Docker

PostgreSQL is included in `docker-compose.yml`:

```bash
docker-compose up postgres
```

### Manual Setup

```bash
# Install PostgreSQL
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Start service
sudo service postgresql start  # Linux
brew services start postgresql  # macOS

# Create database
createdb ds_agent
```

### Run Migrations

```bash
cd backend
alembic upgrade head
```

### Database Schema

**Tables:**
- `queries`: User queries and responses
- `datasets`: Cached dataset metadata
- `api_logs`: All API request logs
- `sessions`: Session information

## Firebase (Alternative)

### Setup

1. Create Firebase project at https://console.firebase.google.com
2. Enable Firestore Database
3. Download service account key as `firebase-credentials.json`
4. Place in backend root directory

### Configuration

```python
# In backend/app/db/database.py
firebase_db = get_firebase_db()

# Store query
firebase_db.collection('queries').add({
    'session_id': session_id,
    'query': query_text,
    'timestamp': firestore.SERVER_TIMESTAMP
})
```

### Collections Structure

```
queries/
  {query_id}/
    - session_id
    - query_text
    - results
    - timestamp

datasets/
  {dataset_id}/
    - title
    - description
    - access_count

sessions/
  {session_id}/
    - user_id
    - context
    - created_at
```

## Querying Data

### PostgreSQL

```python
from app.db.database import get_db
from app.db.repository import QueryRepository

db = next(get_db())
queries = QueryRepository.get_session_queries(db, session_id)
```

### Firebase

```python
from app.db.database import get_firebase_db

db = get_firebase_db()
queries = db.collection('queries')\
    .where('session_id', '==', session_id)\
    .order_by('timestamp', direction='DESCENDING')\
    .limit(10)\
    .stream()
```

## Analytics Queries

### Most Popular Datasets
```sql
SELECT dataset_id, title, access_count 
FROM datasets 
ORDER BY access_count DESC 
LIMIT 10;
```

### Average Query Execution Time
```sql
SELECT AVG(execution_time) as avg_time,
       COUNT(*) as total_queries
FROM queries 
WHERE status = 'completed';
```

### Error Rate
```sql
SELECT 
    COUNT(CASE WHEN status = 'error' THEN 1 END) * 100.0 / COUNT(*) as error_rate
FROM queries;
```

## Backup & Restore

### PostgreSQL
```bash
# Backup
pg_dump ds_agent > backup.sql

# Restore
psql ds_agent < backup.sql
```

### Firebase
Use Firebase Console → Firestore → Import/Export
