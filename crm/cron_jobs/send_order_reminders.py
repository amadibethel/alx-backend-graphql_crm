#!/usr/bin/env python3
"""
Script: send_order_reminders.py
Description:
    Uses the gql library to query the GraphQL endpoint for orders placed within
    the last 7 days, logs each order’s ID and customer email to a log file with
    a timestamp, and prints "Order reminders processed!" to the console.
"""

import datetime
import asyncio
import logging
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Configure logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# Calculate date range
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)

# Define GraphQL query
query = gql("""
query {
  orders(orderDate_Gte: "%s", orderDate_Lte: "%s") {
    id
    customer {
      email
    }
  }
}
""" % (seven_days_ago, today))

async def fetch_orders():
    try:
        # Define transport and client
        transport = AIOHTTPTransport(url=GRAPHQL_ENDPOINT)
        async with Client(transport=transport, fetch_schema_from_transport=True) as session:
            result = await session.execute(query)
            orders = result.get("orders", [])
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

if __name__ == "__main__":
    asyncio.run(fetch_orders())

