# Simple Deployment Guide

## Build & Deploy

### 1. Build Docker Image
```bash
# Don't forget the dot (.) at the end!
docker build -t command-search:latest .
```

### 2. Test Locally
```bash
docker run -p 8501:8501 command-search:latest
```
Visit: http://localhost:8501

### 3. Deploy with Helm
```bash
# Install
helm install my-app ./helm

# Upgrade
helm upgrade my-app ./helm

# Uninstall
helm uninstall my-app
```

### 4. Access Application
```bash
# Port forward to access locally
kubectl port-forward service/command-search 8080:80

# Visit: http://localhost:8080
```

## Files Created
- `Dockerfile` - Container image
- `requirements.txt` - Python dependencies
- `helm/` - Kubernetes deployment files
