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
