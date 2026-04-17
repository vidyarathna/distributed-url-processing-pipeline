# 🚀 Distributed URL Processing Pipeline

A Redis-backed asynchronous job processing system built with FastAPI and worker-based architecture.

This project demonstrates how to handle **concurrent I/O-bound tasks**, **retry failures**, and build a **queue-driven backend system**.

---

## 🧠 Overview

* Users submit URLs via API
* Jobs are pushed into a Redis queue
* Workers consume and process jobs asynchronously
* Failed jobs are retried with a limit

---

## 🏗️ Architecture

```
Client → FastAPI → Redis Queue → Worker → External URLs
```

---

## ⚙️ Tech Stack

* Backend: FastAPI
* Queue: Redis
* Worker: Python
* HTTP Client: httpx
* Container: Docker

---

## 📁 Project Structure

```
distributed-url-processing-pipeline/
│
├── app/
│   └── main.py
│
├── worker/
│   └── worker.py
│
├── requirements.txt
└── README.md
```

---

## 🔧 Prerequisites

* Python 3.9+
* Docker
* Git

---

## 📦 Setup & Run

### 1. Clone Repository

```
git clone https://github.com/vidyarathna/distributed-url-processing-pipeline.git
cd distributed-url-processing-pipeline
```

---

### 2. Create Virtual Environment

```
python -m venv venv
```

#### Activate:

**Windows:**

```
venv\Scripts\activate
```

**Mac/Linux:**

```
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Start Redis (Docker)

```
docker run -d -p 6379:6379 redis
```

#### Verify:

```
docker ps
```

---

### 5. Clear Queue (Optional but Recommended)

```
docker exec -it <container_id> redis-cli
```

Inside Redis:

```
DEL job_queue
exit
```

---

### 6. Start API Server

```
uvicorn app.main:app
```

API available at:

```
http://127.0.0.1:8000
```

---

### 7. Start Worker (New Terminal)

```
python worker/worker.py
```

Expected:

```
Worker started... Waiting for jobs...
```

---

### 8. Trigger Jobs

Open:

```
http://127.0.0.1:8000/docs
```

* Select `POST /submit`
* Click **Try it out → Execute**

---

### 9. Worker Output Example

```
[PROCESSING] https://example.com | Retry: 0
[SUCCESS] https://example.com | Status: 200

[PROCESSING] https://google.com | Retry: 0
[RETRY] https://google.com | Attempt: 1

[PROCESSING] https://google.com | Retry: 1
[SUCCESS] https://google.com | Status: 200
```

---

## 🔁 Features

* Redis-based job queue
* Asynchronous worker processing
* Retry mechanism with limits
* Failure simulation and handling
* Concurrent I/O task execution

---

## ⚠️ Important Notes

* Worker waits silently if no jobs exist
* Jobs are removed after processing (no persistence yet)
* Do not stop worker during execution

---

## 🛑 Stopping Services

Stop API / Worker:

```
CTRL + C
```

Stop Redis:

```
docker stop <container_id>
```

---

## 🚀 Future Improvements

* Add PostgreSQL for job tracking
* Add job status APIs
* Add metrics and monitoring
* Add multiple workers for scaling

---

## 🧠 What This Project Demonstrates

* Queue-based system design
* Handling unreliable external calls
* Retry and failure recovery strategies
* Separation of producer and consumer systems

---

## 📌 Author

Vidyarathna B
GitHub: https://github.com/vidyarathna
