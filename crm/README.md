# CRM Weekly Report Task

## Setup Steps

1. Install Redis:
   ```bash
   sudo apt-get install redis-server
   redis-server

Install Python dependencies:

pip install -r requirements.txt



Apply Django migrations:

python manage.py migrate



Start Celery worker:

celery -A crm worker -l info



Start Celery Beat:

celery -A crm beat -l info



Verify logs:

tail -f /tmp/crm_report_log.txt




---

## Summary of Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Add `celery` and `django-celery-beat` |
| `crm/celery.py` | Initialize Celery app with Redis |
| `crm/__init__.py` | Load Celery app automatically |
| `crm/tasks.py` | Define `generate_crm_report` Celery task using GraphQL |
| `crm/settings.py` | Add Celery/Beat configuration |
| `crm/README.md` | Document how to setup and run the Celery weekly report |

---

This setup ensures:  

Celery tasks are configured  
Celery Beat schedules the weekly report  
Logs are written to `/tmp/crm_report_log.txt`  
Uses GraphQL queries per requirement  

---

Install Redis and dependencies

Your README includes:

sudo apt-get install redis-server
redis-server
pip install -r requirements.txt


Run migrations

Your README includes:

python manage.py migrate


Start Celery worker

Your README includes:

celery -A crm worker -l info


Start Celery Beat

Your README includes:

celery -A crm beat -l info


Verify logs

Your README includes:

tail -f /tmp/crm_report_log.txt

