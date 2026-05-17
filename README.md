````markdown
# 🚀 SupportIQ — AI-Powered Customer Support Insight Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)

SupportIQ is an AI-powered customer support insight platform designed for e-commerce and support-based businesses.

The platform analyzes customer support tickets, detects customer sentiment and frustration, categorizes issues, estimates revenue impact, and generates suggested responses for support agents.

---

# 📌 Project Overview

Modern e-commerce companies receive thousands of customer messages through:

- Email
- Chat support
- Website tickets

It becomes difficult for support teams to identify:

- Common customer complaints
- Increasing issue trends
- Revenue-impacting problems
- Urgent frustrated customers
- Best response strategies

SupportIQ converts raw customer messages into actionable business insights using AI and analytics.

---

# 🌐 Live Deployment

## Frontend Dashboard

```text
https://supportiq-frontend.onrender.com
```

## Backend API Documentation

```text
https://supportiq-backend-7ouo.onrender.com/docs
```

## Backend Health Check

```text
https://supportiq-backend-7ouo.onrender.com/health
```

---

# 🎥 Project Demo

```text
https://drive.google.com/file/d/1wB7A24wh-dXUK1CV9yQhVZkmdury6LMQ/view?usp=drive_link
```

---

# 🔗 GitHub Repository

```text
https://github.com/SurojuAkshayKumar/supportiq
```

---

# 📂 Dataset Information

The project uses a public spam/ham email dataset as the base dataset.

### Dataset Includes

- 5,171 email messages
- Spam/Ham labels
- Email text content

The dataset was enriched into a customer-support style dataset.

### Additional Fields Added

- `ticket_id`
- `timestamp`
- `customer_id`
- `channel`
- `product`
- `order_value`
- `customer_country`
- `resolution_status`
- `agent_reply`

---

# 🧠 AI Features

The AI pipeline performs:

- ✅ Text Cleaning
- ✅ Data Enrichment
- ✅ Ticket Categorization
- ✅ Sentiment Detection
- ✅ Frustration Detection
- ✅ Revenue Impact Analysis
- ✅ Recurring Issue Extraction
- ✅ Suggested Response Generation

---

# 🏷️ Ticket Categories

SupportIQ classifies tickets into categories such as:

- Delivery Delay
- Refund Issue
- Damaged Product
- Wrong Item
- Payment Failure
- Return/Exchange
- Product Quality
- Account/Login Issue
- Technical Issue
- Promotional/Spam
- Positive Feedback
- General Inquiry

---

# 🏗️ Software Architecture

The project contains:

- FastAPI Backend
- Streamlit Frontend
- AI Processing Pipeline
- SQLite Database

---

# ⚙️ Backend APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/upload` | Upload tickets |
| POST | `/process` | Process tickets |
| GET | `/insights` | Retrieve insights |
| GET | `/tickets` | Fetch tickets |
| POST | `/suggest-response` | Generate AI response |

---

# 📊 Frontend Dashboard Features

The Streamlit dashboard provides:

- Backend Status
- Upload & Process Tickets
- Business Overview
- Top Issues
- Sentiment Trends
- Ticket Summaries
- Suggested Responses
- Live Response Generator

---

# 🔄 Data Pipeline Flow

```text
Raw Dataset
    ↓
Data Cleaning
    ↓
Data Enrichment
    ↓
AI Analysis
    ↓
CSV + SQLite Storage
    ↓
FastAPI Backend
    ↓
Streamlit Dashboard
```

---

# 📁 Project Structure

```text
supportiq/
│
├── ai_support_pipeline.py
├── backend_api.py
├── app.py
├── database_pipeline.py
│
├── spam_ham_dataset.csv
├── processed_tickets.csv
├── supportiq.db
│
├── Dockerfile
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
│
├── requirements.txt
├── README.md
│
├── ques1_explaination.txt
├── ques2_explaination.txt
├── ques3_explaination.txt
├── question4_explanation.txt
├── question5_business_thinking.txt
├── design_document.md
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core Programming |
| FastAPI | Backend APIs |
| Streamlit | Frontend Dashboard |
| Pandas | Data Processing |
| Plotly | Visualization |
| SQLite | Database |
| Docker | Containerization |
| GitHub Actions | CI/CD |
| Render | Cloud Deployment |

---

# ▶️ Running Locally

## 1️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment (Windows)

```bash
venv\Scripts\activate
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run AI Processing Pipeline

```bash
python ai_support_pipeline.py
```

Creates:

```text
processed_tickets.csv
```

---

## 4️⃣ Run Database Pipeline

```bash
python database_pipeline.py
```

Creates:

```text
supportiq.db
```

---

## 5️⃣ Start FastAPI Backend

```bash
uvicorn backend_api:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## 6️⃣ Start Streamlit Frontend

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 🐳 Running with Docker

Make sure Docker Desktop is running.

```bash
docker compose up --build --force-recreate
```

## Docker URLs

### Backend API Docs

```text
http://127.0.0.1:8010/docs
```

### Frontend Dashboard

```text
http://127.0.0.1:8520
```

### Stop Containers

```bash
docker compose down
```

---

# ☁️ Cloud Deployment

The project is deployed on Render using Docker-based services.

## Backend Deployment

Uses:

```text
Dockerfile.backend
```

Backend URL:

```text
https://supportiq-backend-7ouo.onrender.com
```

---

## Frontend Deployment

Uses:

```text
Dockerfile.frontend
```

Frontend URL:

```text
https://supportiq-frontend.onrender.com
```

---

# 🔄 CI/CD Pipeline

GitHub Actions workflow:

```text
.github/workflows/ci.yml
```

Pipeline performs:

- Repository checkout
- Python setup
- Dependency installation
- AI pipeline execution
- Database pipeline execution
- Docker image build
- CI validation

---

# 📈 Business Value

SupportIQ helps businesses by providing:

- Top complaint categories
- Sentiment trends
- Frustration analytics
- Revenue impact insights
- Suggested support responses
- Ticket prioritization

Benefits include:

- Faster agent responses
- Reduced support costs
- Improved customer satisfaction
- Better retention
- Faster issue resolution

---

# 📊 Key Metrics Tracked

- Total ticket volume
- Tickets by category
- Sentiment distribution
- Frustration distribution
- Revenue impact by issue
- Critical ticket count
- Resolution status
- Recurring issue keywords

---

# 🧱 System Architecture

```text
Raw Dataset
spam_ham_dataset.csv
        ↓
AI Processing Pipeline
ai_support_pipeline.py
        ↓
Cleaning + Enrichment + AI Analysis
        ↓
processed_tickets.csv + supportiq.db
        ↓
FastAPI Backend
backend_api.py
        ↓
Streamlit Frontend Dashboard
app.py
        ↓
Business Users / Support Agents

Deployment Layer:
GitHub → GitHub Actions → Docker → Render
```

---

# ⚠️ Current Limitations

This project is currently a prototype.

### Future Improvements

- PostgreSQL integration
- LLM-based response generation
- Vector databases & embeddings
- Real-time streaming
- Authentication system
- Advanced monitoring
- Auto-scaling deployment

---

# 📦 Final Deliverables

- GitHub Repository
- Deployed Frontend
- Deployed Backend APIs
- Architecture Diagram
- Demo Video
- Design Document

---

# 👨‍💻 Author

## Suroju Akshay Kumar

AI-Powered Customer Support Insight Platform Project
````
