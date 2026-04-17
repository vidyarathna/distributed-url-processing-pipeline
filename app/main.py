# app/main.py

"""
API LAYER (Producer)

Purpose:
- Accept incoming requests
- Convert them into jobs
- Push jobs into Redis queue
- DO NOT process jobs here (non-blocking design)

Design Goal:
- Keep API fast and responsive
- Offload heavy work to background workers

Architecture Role:
Client → API (this file) → Redis Queue → Worker
"""

from fastapi import FastAPI
import redis
import json

app = FastAPI()

# Redis connection
# decode_responses=True → ensures Redis returns strings instead of bytes
# Important for JSON parsing
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Central queue name
# Must match worker exactly → otherwise system breaks
QUEUE_NAME = "job_queue"


@app.get("/")
def home():
    """
    Health check endpoint

    Why needed:
    - Verify API is running
    - Used in monitoring / load balancers
    """
    return {"message": "API running"}


@app.post("/submit")
def submit_jobs():
    """
    Job submission endpoint

    Responsibilities:
    - Accept input (currently hardcoded for simplicity)
    - Convert each URL into a job payload
    - Push jobs into Redis queue

    Design Decision:
    - API does NOT wait for processing
    - Returns immediately after enqueue

    This makes system:
    - scalable
    - non-blocking
    """

    # Example input (can be replaced with request body later)
    urls = [
        "https://example.com",
        "https://google.com",
        "https://github.com"
    ]

    for url in urls:
        # Job payload structure
        # This is a CONTRACT between API and worker
        job_data = {
            "url": url,

            # retry_count is REQUIRED
            # Worker depends on it for retry logic
            # Missing this → system crash (you already saw this bug)
            "retry_count": 0
        }

        # Push job into Redis queue
        # LPUSH → adds to left
        # Worker uses BRPOP → consumes from right (FIFO behavior)
        redis_client.lpush(QUEUE_NAME, json.dumps(job_data))

    return {"message": "Jobs added to queue"}