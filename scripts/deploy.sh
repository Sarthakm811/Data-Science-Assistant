#!/bin/bash
set -e

echo "🚢 Deploying Data Science Research Assistant Agent to Kubernetes"
echo ""

# Check prerequisites
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl is required"; exit 1; }

# Check cluster connection
if ! kubectl cluster-info > /dev/null 2>&1; then
    echo "❌ Cannot connect to Kubernetes cluster"
    exit 1
fi

echo "✅ Connected to Kubernetes cluster"
echo ""

# Create namespace if it doesn't exist
kubectl create namespace ds-agent --dry-run=client -o yaml | kubectl apply -f -

# Create secrets
echo "🔐 Creating secrets..."
kubectl create secret generic api-secrets \
  --from-literal=gemini-api-key=${GEMINI_API_KEY} \
  --from-literal=kaggle-username=${KAGGLE_USERNAME} \
  --from-literal=kaggle-key=${KAGGLE_KEY} \
  --namespace=ds-agent \
  --dry-run=client -o yaml | kubectl apply -f -

# Apply configurations
echo "📦 Applying Kubernetes manifests..."
kubectl apply -f infra/k8s/ --namespace=ds-agent

echo ""
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s \
  deployment/ds-agent-backend \
  deployment/ds-agent-frontend \
  --namespace=ds-agent

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Check status:"
echo "  kubectl get pods -n ds-agent"
echo "  kubectl get services -n ds-agent"
echo ""
echo "View logs:"
echo "  kubectl logs -l app=ds-agent-backend -n ds-agent -f"
