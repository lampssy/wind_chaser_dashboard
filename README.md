# Wind Chaser Dashboard

This repository contains the FastAPI application for the Wind Chaser project. The dashboard provides a user interface for monitoring windsurfing sessions, performance metrics, and weather conditions.

## Getting Started

### Prerequisites

- Python 3.12
- Poetry

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-org/wind_chaser_dashboard.git
   cd wind_chaser_dashboard

2. Install dependencies:
   ```sh
   poetry install

3. Run the application:
    ```sh
    poetry run uvicorn app:app --host 0.0.0.0 --port 8000

### Docker
To build and run the Docker container:

1. Build the Docker image:
   ```sh
   docker build -t wind_chaser_dashboard .

2. Run the Docker container:
   ```sh
    docker run -d -p 8000:80 wind_chaser_dashboard

### Kubernetes
To deploy the dashboard using Kubernetes, apply the following files:

1. Deployment:
    ```sh
    kubectl apply -f k8s/deployment.yaml

2. Service:
    ```sh
    kubectl apply -f k8s/service.yaml

3. (Optional) Ingress:
    ```sh
    kubectl apply -f k8s/ingress.yaml