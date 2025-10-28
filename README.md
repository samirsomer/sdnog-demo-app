
# From Code to Cloud: Building a DevOps Pipeline Step by Step 🚀

This repository is used for the **DevOps Workshop: From Code to Cloud**, where we build and deploy a fully observable FastAPI application using **Jenkins**, **Terraform**, **Docker**, and **Grafana stack** on **DigitalOcean**.

---

## 🧭 Overview

In this workshop, we will:
1. **Build** a Python FastAPI application.
2. **Run CI** stages with linting, testing, and static analysis.
3. **Scan for vulnerabilities** using Trivy and quality gates via SonarQube.
4. **Provision infrastructure** on DigitalOcean using Terraform.
5. **Deploy** the application with Docker Compose.
6. **Enable observability** with OpenTelemetry, Prometheus, Jaeger, Loki, and Grafana.

---

## ⚙️ Architecture

```
+------------------------+
|      GitLab Repo       |
|  (Source & Jenkinsfile)|
+-----------+------------+
            |
            v
+------------------------+
|       Jenkins CI/CD    |
|  Build • Test • Deploy |
+-----------+------------+
            |
            v
+------------------------+
|   Terraform Provision  |
|   (DigitalOcean VM)    |
+-----------+------------+
            |
            v
+----------------------------------------------+
| Docker Compose Stack on the VM               |
|----------------------------------------------|
|  • demo-app (FastAPI + OTEL)                 |
|  • otel-collector                            |
|  • jaeger                                    |
|  • prometheus                                |
|  • grafana                                   |
|  • loki (optional logs)                      |
+----------------------------------------------+
```

---

## 🧱 Repository Structure

```
.
├── Dockerfile                # Build instructions for demo FastAPI app
├── Jenkinsfile               # CI/CD pipeline definition
├── README.md                 # Workshop documentation (this file)
├── docker-compose.yaml       # Local test stack (app only)
├── requirements.txt          # Python dependencies
├── main.py                   # FastAPI application entrypoint
├── tests/                    # Pytest test cases
│   └── test_main.py
│
└── infra/                    # Infrastructure-as-Code and observability
    ├── main.tf               # Terraform droplet definition
    ├── variables.tf          # Terraform input variables
    ├── outputs.tf            # Terraform output values
    ├── init.sh               # Setup script to install Docker and run stack
    ├── docker-compose.yaml   # Full observability stack (used on VM)
    │
    ├── grafana/              # Grafana provisioning configs
    │   └── provisioning/
    │       ├── dashboards/
    │       │   ├── dashboards.yml
    │       │   └── observability.json
    │       └── datasources/
    │           └── datasources.yml
    │
    ├── otel-collector/       # OpenTelemetry Collector config
    │   └── collector-config.yaml
    │
    └── prometheus/           # Prometheus configuration
        └── prometheus.yml
```

---

## 🔧 Prerequisites

Before running the pipeline:
- Docker and Docker Compose installed locally.
- A DigitalOcean account and API token.
- An SSH key uploaded to DigitalOcean.
- Jenkins running (locally or in Docker).
- SonarQube server and Trivy scanner available.
- (Optional) GitLab Container Registry access for image storage.

---

## 🚀 Quickstart (Local Test)

1. **Build and Run App Locally**
   ```
   docker build -t sdnog-demo-app:latest .
   docker compose up -d
   ```

2. **Access the App**
   ```
   http://localhost:3000
   ```

3. **Run Unit Tests**
   ```
   pytest -v
   ```

---

## ☁️ Deployment Pipeline (CI/CD)

The Jenkins pipeline executes the following stages:

1. **Checkout** → Pull source code from GitLab.
2. **Lint & Test** → Run Flake8 and Pytest.
3. **Static Analysis** → Send report to SonarQube.
4. **Security Scan** → Run Trivy on Docker image.
5. **Build & Push** → Build and publish Docker image.
6. **Provision Infra** → Use Terraform to create DigitalOcean VM.
7. **Deploy Stack** → Install Docker and run observability compose.
8. **Health Check** → Verify application status.

---

## 🧠 Observability Stack

| Service | Purpose | Port |
|----------|----------|------|
| **demo-app** | FastAPI application with OTEL tracing | 3000 |
| **otel-collector** | Collects traces and metrics | 4317 |
| **jaeger** | Trace visualization | 16686 |
| **prometheus** | Metrics collection | 9090 |
| **grafana** | Visualization dashboards | 3001 |
| **loki** | (Optional) Log aggregation | 3100 |

### Grafana Login
```
URL: http://<vm-ip>:3001
User: admin
Pass: admin
```

---

## 🧩 Useful Commands

**Run Terraform locally:**
```
cd infra
terraform init
terraform apply -auto-approve
```

**Destroy resources:**
```
terraform destroy -auto-approve
```

**View deployed IP:**
```
terraform output public_ip
```

---

## 🧹 Cleanup

After the workshop:
```
terraform destroy -auto-approve
docker system prune -af
```

---

## 💬 Credits

Developed for the **From Code to Cloud** workshop by *Samir*,  
demonstrating practical DevOps automation with:
- Jenkins
- Terraform
- Docker
- SonarQube
- Trivy
- OpenTelemetry
- Prometheus
- Grafana
- Jaeger
