# 📅 Daily Progress Log

---

## 📆 Date: 2026-04-17

## 🚀 Title: Built Redis-Based Async Job Processing Pipeline

---

## 🎯 Objective

Build a backend system that processes tasks asynchronously using a queue, instead of handling everything inside API requests.

---

## 🧠 What I Did

* Set up project structure using FastAPI and Python
* Integrated Redis as a queue system
* Implemented job submission API (`/submit`)
* Designed job payload structure with `url` and `retry_count`
* Built worker system to consume jobs from Redis
* Implemented blocking queue consumption using `BRPOP`
* Integrated external HTTP calls using httpx
* Added retry mechanism with max retry limit
* Simulated failures to test system robustness
* Handled errors and re-queued failed jobs
* Fixed data contract issue (`retry_count` missing)
* Debugged Redis, Docker, and worker execution issues
* Understood separation of API, queue, and worker processes

---

## ⚙️ Technical Concepts Learned

* Producer–Consumer pattern
* Queue-based architecture
* Asynchronous/background processing
* Fault tolerance using retries
* Handling external API failures
* Blocking vs non-blocking operations
* System design: decoupling components

---

## 🔧 Tools & Technologies Used

* Python
* FastAPI
* Redis
* httpx
* Docker

---

## 🧪 Key Challenges Faced

* Misunderstanding Redis blocking behavior (`BRPOP`)
* Worker crashing due to missing `retry_count`
* Confusion between Docker commands and Redis CLI
* Incorrect API testing using GET instead of POST
* Killing worker prematurely assuming it was stuck

---

## 🛠️ Fixes & Learnings

* Ensured consistent job structure between API and worker
* Learned to debug queue-based systems step-by-step
* Understood importance of not interrupting blocking workers
* Improved debugging approach (checking logs, queue state)

---

## 📊 Current System Capabilities

* Accepts jobs via API
* Queues jobs using Redis
* Processes jobs asynchronously via worker
* Retries failed jobs up to defined limit

---

## ⚠️ Limitations

* No database persistence
* No job status tracking
* No metrics or monitoring
* Single worker (limited scalability)

---

## 🔮 Next Steps

* Add PostgreSQL for job tracking
* Implement job status API
* Add metrics (success rate, processing time)
* Support multiple workers

---

## 🧠 Reflection

Today I moved from basic API development to understanding how real backend systems handle asynchronous processing, failures, and system decoupling.

---
