# SubTrack — Recurring Expense Intelligence Platform

## Executive Summary
SubTrack helps students, freelancers, and professionals manage recurring subscriptions from one dashboard, reducing unnoticed financial leakage from auto-renewals and forgotten free trials.

## Problem Statement
Users often underestimate subscription spending because bills are fragmented across services and dates. Free trials and recurring charges are easy to forget, leading to unnecessary costs.

## Proposed Solution
A Django-based web system that provides:
- Centralized subscription tracking.
- Billing reminders before renewal.
- Spending forecasts for monthly/annual/5-year horizons.
- Usage insights to detect potentially wasted subscriptions.

## Technical Architecture
- Backend: Python + Django (MVT).
- Database: SQLite (dev) / PostgreSQL (production).
- Frontend: Django Templates + Bootstrap 5 + Chart.js.
- Data Access: Django ORM.

## Core Modules
1. **Authentication**: Sign up, login, logout.
2. **Subscription Management**: CRUD for subscriptions.
3. **Category Management**: Group subscriptions for analysis.
4. **Dashboard & Analytics**: KPIs, charts, upcoming bills.
5. **Notification Engine**: Reminder generation and email dispatch.
6. **Usage Insights**: Track used/not-used monthly status.

## Non-Functional Requirements
- Performance: dashboard loads within ~2 seconds on standard datasets.
- Security: password hashing and built-in auth from Django.
- Usability: responsive Bootstrap UI.
- Scalability: PostgreSQL-ready deployment path.
