#!/bin/bash
# -------------------------------------------------------------------
# Script: clean_inactive_customers.sh
# Description: Deletes customers with no orders in the past year
# and logs the number deleted with a timestamp.
# -------------------------------------------------------------------

# Activate virtual environment if needed (optional)
# source /path/to/venv/bin/activate

# Define log file
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Run Django shell command
cd "$(dirname "$0")/../.."  # Move to project root where manage.py exists

# Run cleanup task through Django shell
python manage.py shell <<EOF
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(orders__isnull=True, date_joined__lt=one_year_ago)

count = inactive_customers.count()
inactive_customers.delete()

print(f"{timezone.now()}: Deleted {count} inactive customers.")
EOF

# Append output to log file
python manage.py shell <<EOF | tee -a "$LOG_FILE"
from django.utils import timezone
print(f"Cleanup executed at {timezone.now()}")
EOF

