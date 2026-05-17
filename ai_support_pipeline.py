import pandas as pd
import random
import re
from collections import Counter
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

PRODUCTS = [
    "Smartphone", "Laptop", "Headphones", "Shoes", "Watch",
    "Backpack", "Camera", "Tablet", "Home Appliance", "Gaming Console"
]

COUNTRIES = [
    "India", "USA", "UK", "Canada", "Australia", "Germany", "Singapore"
]

CHANNELS = ["chat", "email", "web"]

RESOLUTION_STATUSES = ["Open", "Resolved", "Pending", "Escalated"]

CATEGORY_KEYWORDS = {
    "Delivery Delay": [
        "delayed", "delay", "delivery", "shipping", "shipment",
        "package", "late", "tracking", "arrive", "courier"
    ],
    "Refund Issue": [
        "refund", "money back", "credited", "reimbursement",
        "returned money", "chargeback"
    ],
    "Damaged Product": [
        "damaged", "broken", "defective", "faulty",
        "unusable", "cracked", "not working"
    ],
    "Wrong Item": [
        "wrong", "different", "incorrect", "not what i ordered",
        "mismatch", "wrong item"
    ],
    "Payment Failure": [
        "payment", "charged", "transaction", "deducted",
        "billing", "invoice", "paid", "credit card"
    ],
    "Return or Exchange": [
        "return", "exchange", "replace", "replacement", "send back"
    ],
    "Product Quality": [
        "quality", "poor", "bad", "description",
        "unhappy", "not satisfied", "cheap"
    ],
    "Account/Login Issue": [
        "login", "account", "password", "locked",
        "sign in", "signin", "access"
    ],
    "Technical Issue": [
        "error", "bug", "crash", "issue", "problem",
        "not opening", "server", "system"
    ],
    "Promotional/Spam": [
        "free", "offer", "discount", "winner", "click",
        "promotion", "deal", "limited time", "earn money",
        "congratulations", "marketing"
    ]
}

FRUSTRATION_WORDS = [
    "frustrating", "angry", "worst", "terrible", "immediately",
    "urgent", "bad", "disappointed", "unacceptable", "annoyed",
    "asap", "complaint"
]


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"subject:", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def categorize_ticket(message, original_label):
    clean_msg = clean_text(message)

    # Use original spam label as extra signal
    if str(original_label).lower() == "spam":
        return "Promotional/Spam"

    # Positive feedback should not be treated as a complaint
    positive_words = [
        "thank you", "thanks", "happy", "excellent", "great",
        "good", "amazing", "quick delivery", "fast delivery",
        "satisfied", "love", "perfect", "best service"
    ]

    positive_count = 0
    for word in positive_words:
        if word in clean_msg:
            positive_count += 1

    sentiment, sentiment_score = detect_sentiment(message)

    if sentiment_score >= 0.4 and positive_count >= 1:
        return "Positive Feedback"

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in clean_msg:
                score += 1
        scores[category] = score

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "General Inquiry"

    return best_category


def detect_sentiment(message):
    score = analyzer.polarity_scores(str(message))["compound"]

    if score >= 0.3:
        return "Positive", score
    elif score <= -0.5:
        return "Very Negative", score
    elif score < 0:
        return "Negative", score
    else:
        return "Neutral", score


def detect_frustration(message, sentiment_score):
    clean_msg = clean_text(message)
    frustration_count = 0

    for word in FRUSTRATION_WORDS:
        if word in clean_msg:
            frustration_count += 1

    if sentiment_score <= -0.6 or frustration_count >= 2:
        return "Critical"
    elif sentiment_score <= -0.3 or frustration_count == 1:
        return "High"
    elif sentiment_score < 0:
        return "Medium"
    else:
        return "Low"


import pandas as pd
import random
import re
from collections import Counter
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

PRODUCTS = [
    "Smartphone", "Laptop", "Headphones", "Shoes", "Watch",
    "Backpack", "Camera", "Tablet", "Home Appliance", "Gaming Console"
]

COUNTRIES = [
    "India", "USA", "UK", "Canada", "Australia", "Germany", "Singapore"
]

CHANNELS = ["chat", "email", "web"]

RESOLUTION_STATUSES = ["Open", "Resolved", "Pending", "Escalated"]

CATEGORY_KEYWORDS = {
    "Positive Feedback": [
        "thank you", "thanks", "happy", "excellent", "great",
        "good", "amazing", "quick delivery", "fast delivery",
        "satisfied", "love", "perfect", "best service"
    ],
    "Delivery Delay": [
        "delayed", "delay", "delivery", "shipping", "shipment",
        "package", "late", "tracking", "arrive", "courier"
    ],
    "Refund Issue": [
        "refund", "money back", "credited", "reimbursement",
        "returned money", "chargeback"
    ],
    "Damaged Product": [
        "damaged", "broken", "defective", "faulty",
        "unusable", "cracked", "not working"
    ],
    "Wrong Item": [
        "wrong", "different", "incorrect", "not what i ordered",
        "mismatch", "wrong item"
    ],
    "Payment Failure": [
        "payment", "charged", "transaction", "deducted",
        "billing", "invoice", "paid", "credit card"
    ],
    "Return or Exchange": [
        "return", "exchange", "replace", "replacement", "send back"
    ],
    "Product Quality": [
        "quality", "poor", "bad", "description",
        "unhappy", "not satisfied", "cheap"
    ],
    "Account/Login Issue": [
        "login", "account", "password", "locked",
        "sign in", "signin", "access"
    ],
    "Technical Issue": [
        "error", "bug", "crash", "issue", "problem",
        "not opening", "server", "system"
    ],
    "Promotional/Spam": [
        "free", "offer", "discount", "winner", "click",
        "promotion", "deal", "limited time", "earn money",
        "congratulations", "marketing"
    ]
}

FRUSTRATION_WORDS = [
    "frustrating", "angry", "worst", "terrible", "immediately",
    "urgent", "bad", "disappointed", "unacceptable", "annoyed",
    "asap", "complaint"
]


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"subject:", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def categorize_ticket(message, original_label):
    clean_msg = clean_text(message)

    # Use original spam label as extra signal
    if str(original_label).lower() == "spam":
        return "Promotional/Spam"

    # Positive feedback should not be treated as a complaint
    positive_words = [
        "thank you", "thanks", "happy", "excellent", "great",
        "good", "amazing", "quick delivery", "fast delivery",
        "satisfied", "love", "perfect", "best service"
    ]

    positive_count = 0
    for word in positive_words:
        if word in clean_msg:
            positive_count += 1

    sentiment, sentiment_score = detect_sentiment(message)

    if sentiment_score >= 0.4 and positive_count >= 1:
        return "Positive Feedback"

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in clean_msg:
                score += 1
        scores[category] = score

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "General Inquiry"

    return best_category


def detect_sentiment(message):
    score = analyzer.polarity_scores(str(message))["compound"]

    if score >= 0.3:
        return "Positive", score
    elif score <= -0.5:
        return "Very Negative", score
    elif score < 0:
        return "Negative", score
    else:
        return "Neutral", score


def detect_frustration(message, sentiment_score):
    clean_msg = clean_text(message)
    frustration_count = 0

    for word in FRUSTRATION_WORDS:
        if word in clean_msg:
            frustration_count += 1

    if sentiment_score <= -0.6 or frustration_count >= 2:
        return "Critical"
    elif sentiment_score <= -0.3 or frustration_count == 1:
        return "High"
    elif sentiment_score < 0:
        return "Medium"
    else:
        return "Low"


def generate_suggested_response(category):
    responses = {
        "Positive Feedback": "Hi, thank you for your kind feedback. We’re happy to hear that you had a good experience. We appreciate your support and look forward to serving you again.",
        "Delivery Delay": "Hi, I’m sorry for the delivery delay. I’ll check the tracking status and help you with the next available resolution.",
        "Refund Issue": "Hi, I’m sorry your refund has not been completed yet. I’ll review the return and payment status and help make sure the refund is processed as soon as possible.",
        "Damaged Product": "Hi, I’m sorry the product arrived damaged. Please share images of the item and packaging so we can arrange a replacement or refund.",
        "Wrong Item": "Hi, I’m sorry you received the wrong item. I’ll verify your order details and help arrange the correct product or a return.",
        "Payment Failure": "Hi, I understand your concern. I’ll check the transaction status and confirm whether the amount will be refunded or the order can be completed.",
        "Return or Exchange": "Hi, I’ll help you with the return or exchange process. Please confirm your order details and preferred resolution.",
        "Product Quality": "Hi, I’m sorry the product did not meet expectations. I’ll record your feedback and help with the available return, replacement, or refund options.",
        "Account/Login Issue": "Hi, I’ll help you regain access to your account. Please try resetting your password, and I can guide you further if the issue continues.",
        "Technical Issue": "Hi, I’m sorry you are facing a technical issue. I’ll help troubleshoot the problem and escalate it to the technical team if needed.",
        "Promotional/Spam": "This message appears promotional or unrelated to a customer support request. No agent response is required unless the customer provides a valid support concern.",
        "General Inquiry": "Hi, thank you for reaching out. I’ll review your request and help you with the best possible resolution."
    }

    return responses.get(category, responses["General Inquiry"])


def extract_top_issues(messages, top_n=15):
    stopwords = {
        "the", "is", "and", "i", "my", "to", "a", "but", "not",
        "have", "has", "this", "for", "of", "was", "with", "it",
        "in", "after", "many", "need", "help", "you", "your",
        "from", "that", "will", "are", "can", "our", "subject",
        "please", "email", "message", "thanks", "thank", "would",
        "could", "there", "their", "about"
    }

    all_words = []

    for message in messages:
        clean_msg = clean_text(message)
        words = clean_msg.split()

        for word in words:
            if word not in stopwords and len(word) > 3:
                all_words.append(word)

    return Counter(all_words).most_common(top_n)


def add_support_ticket_fields(df):
    enriched_rows = []

    for i, row in df.iterrows():
        original_text = row["text"]
        original_label = row["label"]
        category = categorize_ticket(original_text, original_label)

        if category == "Promotional/Spam":
            order_value = 0
            status = "Closed"
        else:
            order_value = round(random.uniform(20, 1500), 2)
            status = random.choice(RESOLUTION_STATUSES)

        timestamp = datetime.now() - timedelta(days=random.randint(0, 120))

        enriched_rows.append({
            "ticket_id": f"TKT{i+1:05d}",
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "customer_id": f"CUST{random.randint(1000, 9999)}",
            "channel": random.choice(CHANNELS),
            "message": original_text,
            "agent_reply": "",
            "product": random.choice(PRODUCTS),
            "order_value": order_value,
            "customer_country": random.choice(COUNTRIES),
            "resolution_status": status,
            "original_email_label": original_label,
            "original_label_num": row["label_num"]
        })

    return pd.DataFrame(enriched_rows)


def main():
    input_file = "spam_ham_dataset.csv"

    print("Loading dataset...")
    df = pd.read_csv(input_file)

    print("Original dataset loaded successfully.")
    print("Original rows:", len(df))
    print("Original columns:", df.columns.tolist())

    required_columns = {"label", "text", "label_num"}

    if not required_columns.issubset(set(df.columns)):
        raise ValueError("Dataset must contain label, text, and label_num columns.")

    print("\nConverting email dataset into support-ticket format...")
    tickets_df = add_support_ticket_fields(df)

    clean_messages = []
    predicted_categories = []
    sentiments = []
    sentiment_scores = []
    frustration_levels = []
    suggested_responses = []

    print("Running AI analysis...")

    for _, row in tickets_df.iterrows():
        message = row["message"]
        original_label = row["original_email_label"]

        clean_msg = clean_text(message)
        category = categorize_ticket(message, original_label)
        sentiment, score = detect_sentiment(message)
        frustration = detect_frustration(message, score)
        response = generate_suggested_response(category)

        clean_messages.append(clean_msg)
        predicted_categories.append(category)
        sentiments.append(sentiment)
        sentiment_scores.append(score)
        frustration_levels.append(frustration)
        suggested_responses.append(response)

    tickets_df["clean_message"] = clean_messages
    tickets_df["predicted_category"] = predicted_categories
    tickets_df["sentiment"] = sentiments
    tickets_df["sentiment_score"] = sentiment_scores
    tickets_df["frustration_level"] = frustration_levels
    tickets_df["suggested_response"] = suggested_responses

    tickets_df.to_csv("processed_tickets.csv", index=False)

    print("\nAI Processing Completed Successfully.")
    print("Rows processed:", len(tickets_df))
    print("\nFinal output saved as: processed_tickets.csv")

    print("\nSample Output:")
    print(
        tickets_df[
            [
                "ticket_id",
                "predicted_category",
                "sentiment",
                "frustration_level",
                "order_value",
                "suggested_response"
            ]
        ].head()
    )

    print("\nTop Ticket Categories:")
    print(tickets_df["predicted_category"].value_counts())

    print("\nSentiment Summary:")
    print(tickets_df["sentiment"].value_counts())

    print("\nFrustration Level Summary:")
    print(tickets_df["frustration_level"].value_counts())

    print("\nRevenue Impact by Category:")
    revenue_impact = (
        tickets_df.groupby("predicted_category")["order_value"]
        .sum()
        .sort_values(ascending=False)
    )
    print(revenue_impact)

    print("\nTop Recurring Issue Keywords:")
    top_issues = extract_top_issues(tickets_df["message"])
    for word, count in top_issues:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()


def extract_top_issues(messages, top_n=15):
    stopwords = {
        "the", "is", "and", "i", "my", "to", "a", "but", "not",
        "have", "has", "this", "for", "of", "was", "with", "it",
        "in", "after", "many", "need", "help", "you", "your",
        "from", "that", "will", "are", "can", "our", "subject",
        "please", "email", "message", "thanks", "thank", "would",
        "could", "there", "their", "about"
    }

    all_words = []

    for message in messages:
        clean_msg = clean_text(message)
        words = clean_msg.split()

        for word in words:
            if word not in stopwords and len(word) > 3:
                all_words.append(word)

    return Counter(all_words).most_common(top_n)


def add_support_ticket_fields(df):
    enriched_rows = []

    for i, row in df.iterrows():
        original_text = row["text"]
        original_label = row["label"]
        category = categorize_ticket(original_text, original_label)

        if category == "Promotional/Spam":
            order_value = 0
            status = "Closed"
        else:
            order_value = round(random.uniform(20, 1500), 2)
            status = random.choice(RESOLUTION_STATUSES)

        timestamp = datetime.now() - timedelta(days=random.randint(0, 120))

        enriched_rows.append({
            "ticket_id": f"TKT{i+1:05d}",
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "customer_id": f"CUST{random.randint(1000, 9999)}",
            "channel": random.choice(CHANNELS),
            "message": original_text,
            "agent_reply": "",
            "product": random.choice(PRODUCTS),
            "order_value": order_value,
            "customer_country": random.choice(COUNTRIES),
            "resolution_status": status,
            "original_email_label": original_label,
            "original_label_num": row["label_num"]
        })

    return pd.DataFrame(enriched_rows)


def main():
    input_file = "spam_ham_dataset.csv"

    print("Loading dataset...")
    df = pd.read_csv(input_file)

    print("Original dataset loaded successfully.")
    print("Original rows:", len(df))
    print("Original columns:", df.columns.tolist())

    required_columns = {"label", "text", "label_num"}

    if not required_columns.issubset(set(df.columns)):
        raise ValueError("Dataset must contain label, text, and label_num columns.")

    print("\nConverting email dataset into support-ticket format...")
    tickets_df = add_support_ticket_fields(df)

    clean_messages = []
    predicted_categories = []
    sentiments = []
    sentiment_scores = []
    frustration_levels = []
    suggested_responses = []

    print("Running AI analysis...")

    for _, row in tickets_df.iterrows():
        message = row["message"]
        original_label = row["original_email_label"]

        clean_msg = clean_text(message)
        category = categorize_ticket(message, original_label)
        sentiment, score = detect_sentiment(message)
        frustration = detect_frustration(message, score)
        response = generate_suggested_response(category)

        clean_messages.append(clean_msg)
        predicted_categories.append(category)
        sentiments.append(sentiment)
        sentiment_scores.append(score)
        frustration_levels.append(frustration)
        suggested_responses.append(response)

    tickets_df["clean_message"] = clean_messages
    tickets_df["predicted_category"] = predicted_categories
    tickets_df["sentiment"] = sentiments
    tickets_df["sentiment_score"] = sentiment_scores
    tickets_df["frustration_level"] = frustration_levels
    tickets_df["suggested_response"] = suggested_responses

    tickets_df.to_csv("processed_tickets.csv", index=False)

    print("\nAI Processing Completed Successfully.")
    print("Rows processed:", len(tickets_df))
    print("\nFinal output saved as: processed_tickets.csv")

    print("\nSample Output:")
    print(
        tickets_df[
            [
                "ticket_id",
                "predicted_category",
                "sentiment",
                "frustration_level",
                "order_value",
                "suggested_response"
            ]
        ].head()
    )

    print("\nTop Ticket Categories:")
    print(tickets_df["predicted_category"].value_counts())

    print("\nSentiment Summary:")
    print(tickets_df["sentiment"].value_counts())

    print("\nFrustration Level Summary:")
    print(tickets_df["frustration_level"].value_counts())

    print("\nRevenue Impact by Category:")
    revenue_impact = (
        tickets_df.groupby("predicted_category")["order_value"]
        .sum()
        .sort_values(ascending=False)
    )
    print(revenue_impact)

    print("\nTop Recurring Issue Keywords:")
    top_issues = extract_top_issues(tickets_df["message"])
    for word, count in top_issues:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()