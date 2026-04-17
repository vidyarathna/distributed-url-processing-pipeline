# worker/worker.py

"""
WORKER LAYER (Consumer)

Purpose:
- Continuously listen for jobs from Redis queue
- Process jobs independently from API
- Handle failures and retries

Design Goal:
- Decouple processing from request handling
- Enable scalability (multiple workers possible)
- Provide fault tolerance

Architecture Role:
Client → API → Redis → Worker (this file)
"""

import redis
import json
import httpx
import random
import time

# Redis connection (same config as API)
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

QUEUE_NAME = "job_queue"

# Maximum retry attempts before marking job as failed
MAX_RETRIES = 3


def process_job(job: dict):
    """
    Core job processing logic

    Responsibilities:
    - Extract job data
    - Perform actual work (HTTP request here)
    - Raise exception on failure

    Design:
    - Keep this function focused ONLY on processing
    - Retry logic handled outside (separation of concerns)
    """

    url = job["url"]

    # Simulate failure (30%)
    # WHY:
    # - Real systems fail (network issues, timeouts)
    # - You must test retry logic
    if random.random() < 0.3:
        raise Exception("Simulated failure")

    # External API call
    # timeout prevents hanging forever
    # follow_redirects handles 301/302 responses
    response = httpx.get(url, timeout=5, follow_redirects=True)

    print(f"[SUCCESS] {url} | Status: {response.status_code}")


def worker_loop():
    """
    Infinite worker loop

    Behavior:
    - Waits for jobs (blocking)
    - Processes jobs one by one
    - Handles retries on failure

    Important Concept:
    - BRPOP is BLOCKING → waits until job arrives
    - No CPU waste (efficient design)
    """

    print("Worker started... Waiting for jobs...\n")

    while True:
        try:
            # BLOCKING POP
            # Waits until a job is available
            # Returns: (queue_name, job_data)
            _, job_data = redis_client.brpop(QUEUE_NAME)

            # Convert JSON string → Python dict
            job = json.loads(job_data)

            # Defensive read (avoids crash if missing field)
            retry_count = job.get("retry_count", 0)

            print(f"[PROCESSING] {job['url']} | Retry: {retry_count}")

            # Process job
            process_job(job)

        except Exception as e:
            """
            Failure Handling Block

            Handles:
            - network failures
            - simulated failures
            - unexpected errors
            """

            # Increment retry count safely
            job["retry_count"] = job.get("retry_count", 0) + 1

            if job["retry_count"] <= MAX_RETRIES:
                # Retry case
                print(
                    f"[RETRY] {job['url']} | Attempt: {job['retry_count']} | Error: {str(e)}"
                )

                # Small delay prevents tight retry loops
                time.sleep(1)

                # Requeue job for retry
                redis_client.lpush(QUEUE_NAME, json.dumps(job))

            else:
                # Permanent failure
                print(
                    f"[FAILED] {job['url']} | Max retries reached | Error: {str(e)}"
                )


if __name__ == "__main__":
    """
    Entry point

    Allows running worker as standalone process:
    python worker/worker.py
    """
    worker_loop()