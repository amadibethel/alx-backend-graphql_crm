#!/usr/bin/env python3
"""
Script: send_order_reminders.py
Description:
    Queries the GraphQL endpoint for orders placed within the last 7 days,
    logs each order’s ID and customer email to a log file with a timestamp,
    and prints a confirmation message when done.
"""

import datetime
import logging
import requests

# Configure logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# Calculate date range (past 7 days)
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)

# GraphQL query
query = """
query {
  orders(orderDate_Gte: "%s", orderDate_Lte: "%s") {
    id
    customer {
      email
    }
  }
}
""" % (seven_days_ago, today)

try:
    response = requests.post(GRAPHQL_ENDPOINT, json={"query": query})
    response.raise_for_status()
    data = response.json()

    orders = data.get("data", {}).get("orders", [])
    if not orders:
        logging.info("No orders found in the past 7 days.")
    else:
        for order in orders:
            order_id = order.get("id")
            customer_email = order.get("customer", {}).get("email")
            logging.info(f"Reminder sent for Order ID: {order_id}, Customer: {customer_email}")

    print("Order reminders processed!")

except Exception as e:
    logging.error(f"Error processing order reminders: {e}")
    print("Error processing order reminders!")

