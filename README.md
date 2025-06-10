# Homework #3: Containerization with Podman

This repo contains the solution for Homework 3, demonstrating containerization and multi-container setups using Podman and Podman Compose.

## Task Overview

### Task #1: Single Application Containerization 

**Goal:** Create a `Dockerfile` and run a `business_service` within a container. 
**Implementation:** The `business_service` is located in `homework3-app1/`.

###Task #2: Multi-container Setup with Local Network 

**Goal:** Configure interaction between multiple containers using Podman Compose. 
* **Implementation:**
    A `scheduler_service` (in `homework3-scheduler-app/`) periodically calls the `business_service` (every 10 seconds). 
    `compose.yaml` is used to orchestrate both services. 

## Project Structure

```bash
├── homework3-compose/               
│   └── compose.yaml
├── homework3-app1/
│   ├── .env
│   ├── business_service.py
│   ├── client_service.py
│   ├── db_service.py
│   ├── Dockerfile
│   └── requirements.txt
├── homework3-scheduler-app/  
│   ├── Dockerfile
│   ├── scheduler_service.py
│   └── requirements.txt
└── README.md
```

## Run the Project

1.  **Clone the repository and navigate to the `homework3-compose` directory:**
    ```bash
    git clone [https://github.com/maijamana/homework-3.git](https://github.com/maijamana/homework-3.git)
    cd homework3/homework-3-compose
    ```

2.  **Build and start the services:**
    ```bash
    podman compose build --no-cache && podman compose up -d
    ```

## Functionality Verification

1. **`business_service` in browser:** `http://localhost:8000/status` (should return `{"status_check": "operational"}`). 
2. **`scheduler_service` logs:** `podman logs homework3-compose-scheduler_service-1` (should show successful calls to `business_service`).

## Cleanup
Stop and remove containers:
```bash
podman compose down
```
