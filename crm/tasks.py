import datetime
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from celery import shared_task

@shared_task
def generate_crm_report():
    """
    Generates weekly CRM report with total customers, orders, and revenue.
    Logs to /tmp/crm_report_log.txt
    """
    log_file = "/tmp/crm_report_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
        query {
          totalCustomers: customersCount
          totalOrders: ordersCount
          totalRevenue: ordersTotalRevenue
        }
        """)

        result = client.execute(query)
        total_customers = result.get("totalCustomers", 0)
        total_orders = result.get("totalOrders", 0)
        total_revenue = result.get("totalRevenue", 0)

        report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

        with open(log_file, "a") as f:
            f.write(report)

        logging.info("CRM report generated successfully.")

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Error generating report: {e}\n")
        logging.error(f"Error generating CRM report: {e}")

