# PeopleDesk — Employee Management System

A small Flask web app for maintaining an employee directory. It includes sign-in, employee create/read/update/delete, search, input validation, and duplicate email handling. Employee records are stored in SQLite.

**Live demo:** [people-desk-zzyk.onrender.com](https://people-desk-zzyk.onrender.com) (sign-in required)

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>. The local demo login is `admin` / `admin123`. Change it before sharing a deployed app.

To set configuration, copy `.env.example` to `.env` and export its values in your shell (Flask does not load `.env` automatically). The app reads `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and optional `DATABASE_PATH` from the process environment.

## Deploy on Render

1. Push this folder to a GitHub repository.
2. In Render, create a **Web Service** connected to that repository.
3. Set **Build Command** to `pip install -r requirements.txt` and **Start Command** to `gunicorn app:app`.
4. Add environment variables `SECRET_KEY` (a long random value), `ADMIN_USERNAME`, and `ADMIN_PASSWORD` in the service settings.
5. For persistent employee data, attach a persistent disk and set `DATABASE_PATH` to a file on that disk, such as `/var/data/employees.db`.

The default SQLite file is suitable for local development. On hosted services, use a persistent disk (or migrate to managed PostgreSQL) so data survives redeploys. Hosting plan details can change; check the provider's current limits before publishing.

## Resume description

> Built a Flask employee directory with authenticated CRUD operations, SQLite persistence, searchable records, input validation, and duplicate email protection.

List only the features you have personally run and can explain in an interview.
