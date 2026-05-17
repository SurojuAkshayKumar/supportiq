import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="SupportIQ Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("SupportIQ: AI-Powered Customer Support Insight Platform")

st.write(
    "A lightweight application for uploading support tickets, retrieving AI insights, "
    "viewing top issues, sentiment trends, ticket summaries, and suggested agent responses."
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page",
    [
        "Backend Status",
        "Upload & Process Tickets",
        "Business Overview",
        "Top Issues",
        "Sentiment Trends",
        "Ticket Summaries",
        "Suggested Responses",
        "Live Response Generator"
    ]
)


def api_get(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(response.json().get("detail", "API error"))
            return None
    except Exception as e:
        st.error(f"Could not connect to backend API: {e}")
        return None


def api_post(endpoint, files=None, json=None):
    try:
        response = requests.post(f"{API_URL}{endpoint}", files=files, json=json)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(response.json().get("detail", "API error"))
            return None
    except Exception as e:
        st.error(f"Could not connect to backend API: {e}")
        return None


if page == "Backend Status":
    st.header("Backend Status")

    data = api_get("/health")

    if data:
        st.success("Backend API is running.")
        st.json(data)

    st.subheader("Available Backend Endpoints")

    st.code(
        """
GET  /health
POST /upload
POST /process
GET  /insights
GET  /tickets
POST /suggest-response
        """
    )


elif page == "Upload & Process Tickets":
    st.header("Upload & Process Tickets")

    st.write(
        "Upload a CSV dataset. The app supports either the original spam/ham dataset "
        "or a support-ticket style dataset with a message column."
    )

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/csv"
            )
        }

        result = api_post("/upload", files=files)

        if result:
            st.success("File uploaded successfully.")
            st.json(result)

    if st.button("Run AI Processing Pipeline"):
        result = api_post("/process")

        if result:
            st.success("AI processing completed successfully.")
            st.json(result)

    st.info(
        "If you do not upload a new file, the backend will use spam_ham_dataset.csv "
        "if it exists in the project folder."
    )


elif page == "Business Overview":
    st.header("Business Overview")

    insights = api_get("/insights")

    if insights:
        col1, col2 = st.columns(2)

        col1.metric("Total Tickets", f"{insights['total_tickets']:,}")
        col2.metric(
            "Total Revenue Impact",
            f"${insights['total_revenue_impact']:,.2f}"
        )

        st.subheader("Top Recurring Keywords")

        keywords_df = pd.DataFrame(insights["top_recurring_keywords"])

        if not keywords_df.empty:
            st.dataframe(keywords_df)

        st.subheader("Raw Insights JSON")
        with st.expander("View API Response"):
            st.json(insights)


elif page == "Top Issues":
    st.header("Top Customer Issues")

    insights = api_get("/insights")

    if insights:
        top_issues_df = pd.DataFrame(insights["top_issues"])

        fig = px.bar(
            top_issues_df,
            x="category",
            y="count",
            title="Top Issue Categories",
            labels={"category": "Issue Category", "count": "Ticket Count"}
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Issue Count Table")
        st.dataframe(top_issues_df)

        revenue_df = pd.DataFrame(insights["revenue_impact"])

        st.subheader("Revenue Impact by Issue Category")

        fig2 = px.bar(
            revenue_df,
            x="category",
            y="revenue_impact",
            title="Revenue Impact by Issue Category",
            labels={
                "category": "Issue Category",
                "revenue_impact": "Revenue Impact"
            }
        )

        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(revenue_df)


elif page == "Sentiment Trends":
    st.header("Sentiment and Frustration Trends")

    insights = api_get("/insights")

    if insights:
        sentiment_df = pd.DataFrame(insights["sentiment_summary"])

        fig = px.pie(
            sentiment_df,
            names="sentiment",
            values="count",
            title="Sentiment Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        frustration_df = pd.DataFrame(insights["frustration_summary"])

        fig2 = px.bar(
            frustration_df,
            x="frustration_level",
            y="count",
            title="Frustration Level Summary",
            labels={
                "frustration_level": "Frustration Level",
                "count": "Ticket Count"
            }
        )

        st.plotly_chart(fig2, use_container_width=True)


elif page == "Ticket Summaries":
    st.header("Ticket Summaries")

    insights = api_get("/insights")

    categories = ["All"]

    if insights:
        categories += [item["category"] for item in insights["top_issues"]]

    selected_category = st.selectbox("Filter by category", categories)

    tickets_response = api_get(f"/tickets?limit=100&category={selected_category}")

    if tickets_response:
        tickets_df = pd.DataFrame(tickets_response["tickets"])

        st.write(f"Showing {len(tickets_df)} tickets")
        st.dataframe(tickets_df)


elif page == "Suggested Responses":
    st.header("Suggested Agent Responses")

    tickets_response = api_get("/tickets?limit=30")

    if tickets_response:
        tickets_df = pd.DataFrame(tickets_response["tickets"])

        if tickets_df.empty:
            st.warning("No tickets found.")
        else:
            for _, row in tickets_df.iterrows():
                st.markdown("---")
                st.subheader(f"Ticket: {row.get('ticket_id', 'N/A')}")
                st.write("**Category:**", row.get("predicted_category", "N/A"))
                st.write("**Sentiment:**", row.get("sentiment", "N/A"))
                st.write("**Frustration Level:**", row.get("frustration_level", "N/A"))

                st.write("**Customer Message:**")
                st.write(row.get("message", "N/A"))

                st.write("**Suggested Agent Response:**")
                st.success(row.get("suggested_response", "N/A"))


elif page == "Live Response Generator":
    st.header("Live Suggested Response Generator")

    st.write(
        "Enter a new customer message. The backend will categorize it, detect sentiment, "
        "detect frustration, and generate a suggested agent response."
    )

    message = st.text_area(
        "Customer message",
        placeholder="Example: My payment failed but money was deducted from my account."
    )

    if st.button("Analyze Message"):
        if message.strip():
            result = api_post(
                "/suggest-response",
                json={"message": message}
            )

            if result:
                st.subheader("AI Analysis Result")

                col1, col2, col3 = st.columns(3)

                col1.metric("Category", result["predicted_category"])
                col2.metric("Sentiment", result["sentiment"])
                col3.metric("Frustration", result["frustration_level"])

                st.write("**Suggested Agent Response:**")
                st.success(result["suggested_response"])

                with st.expander("View Full API Response"):
                    st.json(result)
        else:
            st.warning("Please enter a customer message.")

