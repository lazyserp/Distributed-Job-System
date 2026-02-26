USER                    API (redis_api.py)          REDIS              WORKER (worker.py)
  │                            │                       │                       │
  │  POST /submit?duration=5   │                       │                       │
  │───────────────────────────►│                       │                       │
  │                            │                       │                       │
  │                            │  SET job_id "Pending" │                       │
  │                            │──────────────────────►│                       │
  │                            │                       │                       │
  │                            │  LPUSH "job_queue"    │                       │
  │                            │──────────────────────►│                       │
  │                            │                       │                       │
  │◄─── {"job_id": "abc..."}───│                       │                       │
  │                            │                       │                       │
  │                            │                       │    BRPOP (blocking)   │
  │                            │                       │◄──────────────────────│
  │                            │                       │                       │
  │                            │                       │  Returns job data     │
  │                            │                       │──────────────────────►│
  │                            │                       │                       │
  │                            │                       │    SET job_id         │
  │                            │                       │    "Processing"       │
  │                            │                       │◄──────────────────────│
  │                            │                       │                       │
  │                            │                       │         sleep(5)      │
  │                            │                       │                       │
  │  GET /status/abc...        │                       │                       │
  │───────────────────────────►│                       │                       │
  │                            │                       │                       │
  │                            │  GET job_id           │                       │
  │                            │──────────────────────►│                       │
  │                            │                       │                       │
  │                            │◄── "Processing"───────│                       │
  │                            │                       │                       │
  │◄─── {"status": "Processing"}                       │                       │
  │                            │                       │                       │
  │                            │                       │    SET job_id         │
  │                            │                       │    "Completed"        │
  │                            │                       │◄──────────────────────│
  │                            │                       │                       │
  │  GET /status/abc...        │                       │                       │
  │───────────────────────────►│                       │                       │
  │                            │                       │                       │
  │                            │  GET job_id           │                       │
  │                            │──────────────────────►│                       │
  │                            │                       │                       │
  │                            │◄── "Completed"────────│                       │
  │                            │                       │                       │
  │◄─── {"status": "Completed"}                        │                       │