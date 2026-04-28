# Deployment Plan

This application is a FastAPI backend built with Python and produces a containerized API server via Docker.

## Containerize the app

1. Use a `Dockerfile` that:
   - Uses a Python image to install dependencies and run the app
   - Exposes the API on port 8000 using uvicorn

## Azure deployment approach

1. Build the image locally or in CI:
   - `docker build -t backend-app .`
2. Push the image to Azure Container Registry (ACR).
3. Deploy the image using:
   - **Azure Kubernetes Service (AKS)**: if you need Kubernetes orchestration.
4. Configure TLS using Azure-managed certificates or App Service SSL bindings.
5. Optionally put Azure Front Door or Azure CDN in front to improve performance and global delivery.
6. Set up Azure Database for PostgreSQL and Azure Cache for Redis as managed services.

## CI/CD and environment notes

- Use GitHub Actions or Azure Pipelines to automate:
  - Dependency install (`pip install -r requirements.txt`)
  - `pytest` or similar for testing
  - Docker image build and push
  - Deployment to the target container service
- Configure environment variables for database connections, Redis, secrets, etc.
- For the backend API, ensure CORS is configured for frontend origins, and use environment variables for runtime endpoint values.

## Summary

Deploying this app with containers means packaging the Python app into a container, and running that container on Azure ACI or AKS. The key steps are image build, registry push, and managed container service deployment with HTTPS in front, along with managed database and cache services.

The API will be accessible at `http://<public-ip>:8000`.
