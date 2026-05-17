# SupportIQ Design Document

## 1. AI Choices

For this project, I used a lightweight AI pipeline to analyze customer support tickets and generate useful business insights.

The system performs tasks such as:

- Text cleaning
- Ticket categorization
- Sentiment analysis
- Frustration detection
- Recurring issue detection
- Suggested response generation

For sentiment analysis, I used VADER sentiment analysis because it works well on short customer messages and is fast to run. Since this project is a prototype, I chose a rule-based categorization system instead of a heavy machine learning model. This made the system easier to build, explain, test, and debug.

Suggested responses are generated using predefined response templates based on the ticket category and customer sentiment. This keeps the responses consistent and safe for support usage.

The main goal was to create a practical and understandable AI system instead of building an overly complex model.

---

## 2. Data Model

The project started with a public spam/ham email dataset, which I converted into a customer support style dataset.

Additional support-related fields were added, including:

- ticket_id
- timestamp
- customer_id
- product
- channel
- order_value
- customer_country
- sentiment
- frustration_level
- resolution_status
- suggested_response

The original email text acts as the customer support message.

The processed data is stored in both CSV format and a SQLite database. SQLite was chosen because it is lightweight, easy to set up, and works well for a prototype application.

---

## 3. Scalability

The system was designed in a modular way so that different parts can be improved or scaled later.

The backend is built using FastAPI, which is fast and can support multiple API requests efficiently. Since the frontend and backend are separated, they can be deployed and scaled independently.

Docker was used to containerize the application, making deployment easier across local systems and cloud platforms.

Right now, SQLite is enough for a smaller project, but for a production-level system, PostgreSQL or another scalable database would be a better choice.

The current system is suitable for prototype-level workloads, but the structure allows future improvements without changing the full architecture.

---

## 4. Tradeoffs

One important tradeoff in this project was choosing simplicity over advanced accuracy.

Instead of using large AI models or deep learning systems, I used rule-based logic and lightweight sentiment analysis. While advanced models may produce more accurate results, they would also increase complexity, setup time, and resource usage.

SQLite was selected because it is simple and easy to manage, even though it is not ideal for very large-scale applications.

Template-based suggested responses were also used instead of LLM-generated responses because they are more predictable and easier to control.

These choices helped keep the project lightweight, understandable, and easier to deploy within the assignment timeline.

---

## 5. Future Improvements

Some future improvements for the project include:

- PostgreSQL integration
- LLM-based response generation
- Semantic search using embeddings
- Real-time ticket streaming
- Authentication system
- Monitoring and logging
- Auto-scaling deployment
- Better AI-based ticket classification

The current version focuses on building a complete working prototype with a clean architecture and practical business value.
