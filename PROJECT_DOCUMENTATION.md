# 📄 Project Documentation

## Distributed URL Processing Pipeline

---

## 🎯 Objective

The goal of this project is to design and implement a **distributed asynchronous job processing system** that can:

* Handle multiple tasks concurrently
* Decouple request handling from processing
* Manage failures using retry mechanisms
* Simulate real-world backend system behavior

This project focuses on **system design concepts**, not just API development.

---

## 🧠 Problem Statement

In traditional systems:

* API receives request
* Processes it immediately
* Returns response

This creates issues:

* Blocking operations
* Poor scalability
* Failure handling becomes complex

---

## 💡 Solution Approach

I implemented a **queue-based asynchronous architecture** where:

* API only accepts requests
* Jobs are pushed into a queue
* Workers process jobs independently

---

## 🏗️ System Architecture

```text
Client → FastAPI → Redis Queue → Worker → External API
```

### Components:

1. **Client**

   * Sends job requests (URLs)

2. **API Layer (FastAPI)**

   * Accepts input
   * Pushes jobs to queue
   * Does not process jobs

3. **Queue (Redis)**

   * Stores jobs temporarily
   * Acts as buffer between API and worker

4. **Worker**

   * Continuously listens for jobs
   * Processes tasks asynchronously
   * Handles retries on failure

5. **External System**

   * Target URLs being fetched

---

## ⚙️ Technologies Used

* Python
* FastAPI
* Redis
* httpx
* Docker

---

## 🔄 Workflow

1. User sends request via API
2. API pushes jobs into Redis queue
3. Worker retrieves jobs using blocking pop
4. Worker processes each job
5. If failure occurs:

   * Job is retried up to a limit
6. Final status is printed/logged

---

## 📦 Job Structure

Each job is represented as:

```json
{
  "url": "https://example.com",
  "retry_count": 0
}
```

---

## 🔁 Retry Mechanism

* Each job tracks `retry_count`
* On failure:

  * Increment retry count
  * Re-add job to queue
* Maximum retries: 3

If limit exceeded:

* Job is marked as failed

---

## ⚠️ Failure Handling

Failures are simulated using:

```python
random.random() < 0.3
```

This ensures:

* System is tested under failure conditions
* Retry logic is validated

---

## 🧠 Key Concepts Implemented

### 1. Producer–Consumer Pattern

* API → Producer
* Worker → Consumer

---

### 2. Asynchronous Processing

* API does not wait for task completion

---

### 3. Queue-Based Architecture

* Decouples system components
* Enables scalability

---

### 4. Fault Tolerance

* Retry mechanism
* Failure recovery

---

### 5. External I/O Handling

* Network requests using httpx
* Timeout and redirect handling

---

## 🚀 Features

* Redis-based job queue
* Background worker processing
* Retry mechanism with limit
* Failure simulation
* Concurrent task handling

---

## 📉 Current Limitations

* No database persistence
* No job status tracking
* No metrics or monitoring
* No idempotency handling
* Single worker instance

---

## 🔮 Future Improvements

1. Add PostgreSQL for job tracking
2. Implement job status API
3. Add metrics (success rate, latency)
4. Introduce multiple workers for scalability
5. Add idempotency to prevent duplicate jobs

---

## 🧠 Learning Outcomes

This project helped in understanding:

* How real backend systems handle asynchronous tasks
* Importance of decoupling API and processing
* Handling failures in distributed systems
* Designing scalable architectures
* Implementing queue-based workflows

---

## 📌 Conclusion

This project demonstrates a **production-style backend pattern** using:

* Queue-based processing
* Worker architecture
* Retry and failure handling

It serves as a foundation for building:

* scalable systems
* distributed services
* resilient backend architectures

---
