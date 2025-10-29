import datetime
import logging
import requests

# Optional: GraphQL endpoint check
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    """
    Logs a timestamped heartbeat message every 5 minutes
    and optionally verifies GraphQL endpoint responsiveness.
    """
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Write to log file (append mode)
    with open(log_file, "a") as f:
        f.write(message)

    # Optional GraphQL "hello" query check
    try:
        query = '{"query": "{ hello }"}'
        response = requests.post(GRAPHQL_ENDPOINT, data=query, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            logging.info("GraphQL endpoint responded successfully.")
        else:
            logging.warning(f"GraphQL check failed with status: {response.status_code}")
    except Exception as e:
        logging.error(f"GraphQL heartbeat check failed: {e}")

from gql.transport.requests import RequestsHTTPTransport", "from gql import", "gql", "Client"
"/tmp/low_stock_updates_log.txt"
"updateLowStockProducts"
