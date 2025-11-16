#!/bin/bash
set -e

echo "🧪 Running tests for Data Science Research Assistant Agent"
echo ""

# Backend tests
echo "Testing Backend..."
cd backend
python -m pytest tests/ -v --cov=app --cov-report=term-missing

echo ""
echo "✅ All tests passed!"
