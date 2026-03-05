# SubTrack

SubTrack is a Django-based recurring expense intelligence platform for tracking subscriptions, forecasting costs, and reducing wasted spending.

## Features

- User registration and authentication.
- Subscription CRUD with status (Active / Trial / Cancelled).
- Category management.
- Dashboard with monthly, annual, and 5-year spending forecasts.
- Upcoming billing and trial-end monitoring.
- Usage insights to identify wasted subscriptions.
- Billing reminder generation (dashboard trigger + management command).
- Chart.js-powered spending analytics.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (development), PostgreSQL-compatible setup for production
- **Frontend:** Django Templates, Bootstrap 5, Chart.js
- **ORM:** Django ORM

## Quick Start

1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create an admin account:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

## Reminder Automation

To run reminder notifications manually:

```bash
python manage.py send_due_reminders
```

In production, schedule this command daily with cron or a task scheduler.

## Academic Scope Mapping

This implementation covers:

- Authentication module
- Subscription and category CRUD
- Dashboard and analytics views
- Notification process
- Forecast logic
- Usage-based waste insight
- Non-functional requirements documentation in `docs/PROJECT_PROPOSAL.md`
