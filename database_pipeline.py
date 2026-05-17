import sqlite3
import pandas as pd

PROCESSED_FILE = "processed_tickets.csv"
DATABASE_FILE = "supportiq.db"
TABLE_NAME = "tickets"


def create_database():
    print("Loading processed ticket data...")

    df = pd.read_csv(PROCESSED_FILE)

    print("Rows loaded:", len(df))
    print("Columns:", df.columns.tolist())

    print("\nConnecting to SQLite database...")

    connection = sqlite3.connect(DATABASE_FILE)

    print("Saving processed tickets to database table...")

    df.to_sql(
        TABLE_NAME,
        connection,
        if_exists="replace",
        index=False
    )

    print("Data saved successfully.")

    cursor = connection.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    total_rows = cursor.fetchone()[0]

    print("\nDatabase validation:")
    print("Total rows stored:", total_rows)

    print("\nTicket count by category:")
    category_summary = pd.read_sql_query(
        f"""
        SELECT predicted_category, COUNT(*) AS ticket_count
        FROM {TABLE_NAME}
        GROUP BY predicted_category
        ORDER BY ticket_count DESC
        """,
        connection
    )

    print(category_summary)

    print("\nRevenue impact by category:")
    revenue_summary = pd.read_sql_query(
        f"""
        SELECT predicted_category, SUM(order_value) AS total_revenue_impact
        FROM {TABLE_NAME}
        GROUP BY predicted_category
        ORDER BY total_revenue_impact DESC
        """,
        connection
    )

    print(revenue_summary)

    connection.close()

    print("\nDatabase pipeline completed successfully.")
    print("SQLite database created:", DATABASE_FILE)


if __name__ == "__main__":
    create_database()