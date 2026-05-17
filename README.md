Copy this into your `README.md` file.

````markdown
# SupportIQ: AI-Powered Customer Support Insight Platform

SupportIQ is an AI-powered customer support insight platform built for a mid-sized e-commerce/support company. The system analyzes customer support messages, categorizes issues, detects sentiment and frustration, calculates revenue impact, and generates suggested responses for support agents.

---

## Project Overview

E-commerce companies receive many customer messages through chat, email, and web tickets. It becomes difficult for support teams and leadership to understand:

- What customers are complaining about
- Which issues are increasing
- Which problems affect revenue the most
- How support agents should respond

SupportIQ solves this by converting customer messages into actionable business insights.

---

## Deployed Demo

### Frontend Dashboard

https://supportiq-frontend.onrender.com

### Backend API Documentation

https://supportiq-backend-7ouo.onrender.com/docs

### Backend Health Check

https://supportiq-backend-7ouo.onrender.com/health

---

## GitHub Repository

https://github.com/SurojuAkshayKumar/supportiq

---

## Dataset

The project uses a public spam/ham email dataset as the base text dataset.

The dataset contains:

- 5,171 email messages
- spam/ham labels
- email text

Since the original dataset is email-based and does not directly contain customer support ticket fields, it was enriched into a support-ticket style dataset.

Additional fields added:

- ticket_id
- timestamp
- customer_id
- channel
- product
- order_value
- customer_country
- resolution_status
- agent_reply

The original email text is used as the customer message.

---

## Features

### AI / Data Understanding

The AI pipeline performs:

- Text cleaning
- Data enrichment
- Ticket categorization
- Sentiment detection
- Frustration level detection
- Recurring issue extraction
- Revenue impact calculation
- Suggested agent response generation

Ticket categories include:

- Delivery Delay
- Refund Issue
- Damaged Product
- Wrong Item
- Payment Failure
- Return or Exchange
- Product Quality
- Account/Login Issue
- Technical Issue
- Promotional/Spam
- Positive Feedback
- General Inquiry

---

## Software Application

The project includes a FastAPI backend and Streamlit frontend.

### Backend

The backend is built using FastAPI.

Available API endpoints:

- `GET /health`
- `POST /upload`
- `POST /process`
- `GET /insights`
- `GET /tickets`
- `POST /suggest-response`

### Frontend

The frontend dashboard is built using Streamlit.

Dashboard pages:

- Backend Status
- Upload & Process Tickets
- Business Overview
- Top Issues
- Sentiment Trends
- Ticket Summaries
- Suggested Responses
- Live Response Generator

---

## Data Pipeline

The data pipeline follows this flow:

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
````

Pipeline files:

* `ai_support_pipeline.py` processes the dataset and creates `processed_tickets.csv`
* `database_pipeline.py` stores processed data into SQLite
* `supportiq.db` contains the structured `tickets` table

---

## Tech Stack

* Python
* FastAPI
* Streamlit
* pandas
* Plotly
* VADER Sentiment
* SQLite
* Docker
* GitHub Actions
* Render

---

## Project Structure

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

## How to Run Locally

### 1. Create and activate virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run AI processing pipeline

```bash
python ai_support_pipeline.py
```

This creates:

```text
processed_tickets.csv
```

### 4. Run database pipeline

```bash
python database_pipeline.py
```

This creates:

```text
supportiq.db
```

### 5. Start FastAPI backend

```bash
uvicorn backend_api:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

### 6. Start Streamlit frontend

Open a second terminal and run:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## How to Run with Docker

Make sure Docker Desktop is running.

```bash
docker compose up --build --force-recreate
```

Docker URLs:

```text
Backend API Docs:
http://127.0.0.1:8010/docs

Frontend Dashboard:
http://127.0.0.1:8520
```

Stop containers:

```bash
docker compose down
```

---

## Cloud Deployment

The project is deployed on Render using Docker-based web services.

### Backend

The backend is deployed using:

```text
Dockerfile.backend
```

Backend URL:

```text
https://supportiq-backend-7ouo.onrender.com
```

Backend docs:

```text
https://supportiq-backend-7ouo.onrender.com/docs
```

### Frontend

The frontend is deployed using:

```text
Dockerfile.frontend
```

Frontend URL:

```text
https://supportiq-frontend.onrender.com
```

The frontend connects to the backend using the environment variable:

```text
API_URL=https://supportiq-backend-7ouo.onrender.com
```

---

## CI/CD Pipeline

The project includes a GitHub Actions CI pipeline located at:

```text
.github/workflows/ci.yml
```

The CI pipeline runs on push and pull request to the `main` branch.

It performs:

* Repository checkout
* Python setup
* Dependency installation
* AI pipeline execution
* Database pipeline execution
* Backend Docker image build
* Frontend Docker image build

---

## Business Value

SupportIQ helps leadership and support teams by providing:

* Top complaint categories
* Sentiment and frustration trends
* Revenue impact by issue category
* Ticket-level summaries
* Suggested support responses

The system can reduce support costs by automating ticket categorization, helping agents respond faster, and prioritizing urgent tickets.

It can improve revenue and retention by identifying high-impact customer issues and reducing customer frustration.

---

## Key Metrics Tracked

* Total ticket volume
* Tickets by category
* Sentiment distribution
* Frustration level distribution
* Critical tickets
* Revenue impact by issue category
* Top recurring issue keywords
* Suggested response output
* Resolution status distribution

---

## Architecture

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
GitHub → GitHub Actions CI/CD → Docker → Render Cloud Deployment
```

---

## Limitations

This is a prototype project. The current version uses rule-based categorization, template-based responses, CSV storage, and SQLite.

For production, the system can be improved with:

* PostgreSQL
* LLM-based response generation
* Embeddings and vector search
* Real-time ticket streaming
* Authentication
* Advanced monitoring
* Auto-scaling

---

## Final Deliverables

* GitHub repository
* Running deployed frontend demo
* Running deployed backend API
* Architecture diagram
* 5–10 minute demo video
* Design document

---

## Author

Suroju Akshay Kumar

```
```
