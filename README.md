# Hayai Data Cruncher ⚡

A high-performance, multi-tenant analytics dashboard built with **Django 5**, **PostgreSQL**, **Redis**, and **React (Vite + TypeScript)**. Designed to efficiently aggregate and visualize large volumes of transaction data ($50k+$ records) with sub-15ms response times.

## 📈 Performance Metrics

| Strategy | Data Source | Records Processed | Average Response Time | CPU Load |
| :--- | :--- | :--- | :--- | :--- |
| **Cold Query (Aggregations)** | PostgreSQL Indices | 50,000+ rows | ~75ms | Medium |
| **Hot Query (In-Memory)** | Redis Cache | 50,000+ rows | **3ms - 5ms** | Ultra Low |

## 🏗️ Architectural Decisions (Senior Level)

* **Multi-Tenant Row-Level Isolation:** Data is siloed efficiently using indexed Foreign Keys (`store_id`), preparing the system for SaaS scalability without the overhead of maintaining independent physical databases per client.
* **Database Aggregations over Python Loops:** Financial metrics (LTV, Monthly Revenue, Top Products) are calculated directly in PostgreSQL using advanced ORM aggregations (`Sum`, `Avg`, `Count`, `F expressions`). No heavy model instances are loaded into Python memory, avoiding $N+1$ query issues.
* **Atomic Batch Seeding:** The custom seeder generates 50k+ records in under 4 seconds by wrapping transactions in a single database block (`transaction.atomic`) and flushing data using `bulk_create` in batches of 10k.
* **Domain Events vs Django Signals:** To avoid the hidden side-effects and debugging nightmares of standard Django Signals (which also fail during `bulk_create`), this project implements explicit **Domain Events** (`OrderEventDispatcher`) to handle Redis cache invalidation, ensuring strict data consistency.
* **Strict TypeScript Integration:** Frontend data structures are strictly mapped to backend response payloads to ensure compilation-time safety. Resolvers are alias-locked in Vite to guarantee singleton memory footprint for React core.

## 🛠️ Tech Stack

* **Backend:** Django 5, Django REST Framework, PostgreSQL, Redis, Pytest, Factory Boy.
* **Frontend:** React 19, Vite, TypeScript, TailwindCSS, Recharts, Lucide Icons.

## 🚀 Quick Start (Local Setup)

### 1. Infrastructure (Docker)
Ensure Docker is running, then lift the database and cache layers from the root directory:
```bash
docker-compose up -d