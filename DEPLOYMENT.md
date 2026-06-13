# Deployment Guide

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (optional)
- OpenAI API Key
- Banking API credentials

## Local Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/NextIn035846/Multi-AI-Agent-Banking-System.git
cd Multi-AI-Agent-Banking-System
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Docker Deployment

### 1. Build and Run with Docker Compose

```bash
docker-compose up -d
```

### 2. Access the Application

```
http://localhost:8501
```

## Production Deployment

### AWS ECS

1. Push Docker image to ECR
2. Create ECS task definition
3. Launch ECS service

### Google Cloud Run

```bash
gcloud run deploy multi-ai-banking --source .
```

### Azure Container Instances

```bash
az container create --resource-group myResourceGroup --name multi-ai-banking --image multi-ai-banking:latest
```

## Security Considerations

- Use managed secrets services (AWS Secrets Manager, Google Secret Manager, etc.)
- Enable SSL/TLS encryption
- Implement VPN for API communication
- Enable audit logging
- Regular security scanning with tools like Trivy

## Monitoring

- Set up CloudWatch/Stackdriver logs
- Configure alerts for errors and performance issues
- Monitor API latency and throughput
