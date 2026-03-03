# Distributed Job System

A high-performance, fault-tolerant distributed job scheduling and execution system designed for scalable asynchronous task processing across multiple worker nodes.

---

# Features

- **Distributed Architecture** – Decouples job submission from execution
- **Fault Tolerance** – Automatic retry logic and job reassignment
- **Scalability** – Horizontally scalable worker nodes
- **Concurrency Control** – Distributed locking prevents duplicate execution
- **Monitoring** – Real-time job status tracking (Pending, Running, Completed, Failed)
- **Prioritization** – Supports job priority levels

---

# Architecture
USER                    API (redis_api.py)          REDIS              WORKER (worker.py)      POSTGRES
  │                            │                       │                       │                    │
  │  POST /submit?duration=5   │                       │                       │                    │
  │───────────────────────────►│                       │                       │                    │
  │                            │                       │                       │                    │
  │                            │  INSERT "Pending"     │                       │                    │
  │                            │───────────────────────────────────────────────────────────────────►│
  │                            │                       │                       │                    │
  │                            │  LPUSH "job_queue"    │                       │                    │
  │                            │──────────────────────►│                       │                    │
  │                            │                       │                       │                    │
  │◄─── {"job_id": "abc..."}───│                       │                       │                    │
  │                            │                       │                       │                    │
  │                            │                       │    BRPOP (blocking)   │                    │
  │                            │                       │◄──────────────────────│                    │
  │                            │                       │                       │                    │
  │                            │                       │  Returns job data     │                    │
  │                            │                       │──────────────────────►│                    │
  │                            │                       │                       │                    │
  │                            │                       │                       │ UPDATE "Processing"│
  │                            │                       │                       │───────────────────►│
  │                            │                       │                       │                    │
  │                            │                       │                       │      sleep(5)      │
  │                            │                       │                       │                    │
  │  GET /status/abc...        │                       │                       │                    │
  │───────────────────────────►│                       │                       │                    │
  │                            │                       │                       │                    │
  │                            │  SELECT status        │                       │                    │
  │                            │───────────────────────────────────────────────────────────────────►│
  │                            │                       │                       │                    │
  │                            │◄── "Processing"───────│                       │                    │
  │                            │                       │                       │                    │
  │◄─── {"status": "Processing"}                       │                       │                    │
  │                            │                       │                       │                    │
  │                            │                       │                       │ UPDATE "Completed" │
  │                            │                       │                       │───────────────────►│
  │                            │                       │                       │                    │
  │  GET /status/abc...        │                       │                       │                    │
  │───────────────────────────►│                       │                       │                    │
  │                            │                       │                       │                    │
  │                            │  SELECT status        │                       │                    │
  │                            │───────────────────────────────────────────────────────────────────►│
  │                            │                       │                       │                    │
  │                            │◄── "Completed"────────│                       │                    │
  │                            │                       │                       │                    │
  │◄─── {"status": "Completed"}                        │                       │                    │


  
---

# System Components

## API / Producer

- Receives job requests
- Validates and persists jobs
- Pushes tasks to the message broker

## Scheduler / Master

- Distributes jobs to workers
- Monitors worker heartbeats
- Handles retries and failover

## Workers

- Poll for available jobs
- Execute business logic
- Report job results

---

# Tech Stack

- **Language:** Python / Go / Java / Node.js
- **Storage:** PostgreSQL / MySQL / MongoDB
- **Message Broker:** Redis / RabbitMQ / Kafka
- **Containerization:** Docker & Docker Compose

---

# Prerequisites

- Python 3.9+ / Node 16+ / Go 1.20+
- Docker
- Docker Compose

---


## Clone Repository

```bash
git clone https://github.com/lazyserp/Distributed-Job-System.git
cd Distributed-Job-System

```
---

#Configuration
```bash
DB_HOST=localhost
DB_PORT=5432
BROKER_URL=redis://localhost:6379
RETRY_LIMIT=3

```

#API Usage
##Submit a Job

POST /api/jobs

```bash
{
  "name": "process_video",
  "payload": {
    "file_id": "12345"
  },
  "priority": "high"
}
Check Job Status
GET /api/jobs/{job_id}
{
  "job_id": "abc123",
  "status": "running"
}
```