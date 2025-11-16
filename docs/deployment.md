# Deployment Guide

## Prerequisites

- Kubernetes cluster (GKE, EKS, or AKS)
- kubectl configured
- Docker registry access
- Domain name with DNS configured

## Step 1: Create Secrets

```bash
kubectl create secret generic api-secrets \
  --from-literal=gemini-api-key=YOUR_GEMINI_KEY \
  --from-literal=kaggle-username=YOUR_KAGGLE_USERNAME \
  --from-literal=kaggle-key=YOUR_KAGGLE_KEY
```

## Step 2: Deploy Redis

```bash
kubectl apply -f infra/k8s/redis-deployment.yaml
```

## Step 3: Deploy Backend

```bash
export REGISTRY_URL=your-registry.io
export IMAGE_TAG=latest

envsubst < infra/k8s/backend-deployment.yaml | kubectl apply -f -
```

## Step 4: Deploy Ingress

Update `infra/k8s/ingress.yaml` with your domain names, then:

```bash
kubectl apply -f infra/k8s/ingress.yaml
```

## Step 5: Configure DNS

Point your domains to the ingress load balancer IP:

```bash
kubectl get ingress ds-agent-ingress
```

## Monitoring

### Prometheus & Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

### Access Grafana

```bash
kubectl port-forward svc/prometheus-grafana 3000:80
```

Default credentials: admin/prom-operator

## Scaling

The backend has HPA configured. Monitor with:

```bash
kubectl get hpa backend-hpa
```

## Troubleshooting

### Check logs

```bash
kubectl logs -l app=ds-agent-backend --tail=100
```

### Check pod status

```bash
kubectl get pods
kubectl describe pod <pod-name>
```

### Test connectivity

```bash
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- sh
curl http://backend-service:8000/health
```
