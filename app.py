import os
import sqlite3
from functools import wraps
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("DATABASE_PATH", BASE_DIR / "employees.db"))
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-development-key-change-before-deploying")


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            job_title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = os.environ.get("ADMIN_USERNAME", "admin")
        password = os.environ.get("ADMIN_PASSWORD", "admin123")
        if request.form.get("username", "").strip() == username and request.form.get("password", "") == password:
            session["logged_in"] = True
            destination = request.args.get("next", "")
            if not destination.startswith("/") or destination.startswith("//"):
                destination = url_for("index")
            return redirect(destination)
        flash("Those login details did not match.", "error")
    return render_template("login.html")


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    query = request.args.get("q", "").strip()
    with get_db() as db:
        if query:
            pattern = f"%{query}%"
            employees = db.execute("""SELECT * FROM employees
                WHERE name LIKE ? OR email LIKE ? OR department LIKE ? OR job_title LIKE ?
                ORDER BY name""", (pattern, pattern, pattern, pattern)).fetchall()
        else:
            employees = db.execute("SELECT * FROM employees ORDER BY name").fetchall()
        total = db.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    return render_template("index.html", employees=employees, total=total, query=query)


def employee_form_data():
    return {key: request.form.get(key, "").strip() for key in ("name", "email", "department", "job_title")}


def validate_employee(data):
    if not all(data.values()):
        return "Please fill in every field."
    if "@" not in data["email"] or "." not in data["email"].rsplit("@", 1)[-1]:
        return "Enter a valid email address."
    return None


@app.route("/employees/new", methods=["GET", "POST"])
@login_required
def create_employee():
    data = employee_form_data()
    if request.method == "POST":
        error = validate_employee(data)
        if error:
            flash(error, "error")
        else:
            try:
                with get_db() as db:
                    db.execute("INSERT INTO employees (name, email, department, job_title) VALUES (?, ?, ?, ?)",
                               (data["name"], data["email"].lower(), data["department"], data["job_title"]))
                flash("Employee added.", "success")
                return redirect(url_for("index"))
            except sqlite3.IntegrityError:
                flash("An employee with that email already exists.", "error")
    return render_template("employee_form.html", employee=data, page_title="Add employee", submit_label="Add employee")


@app.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
@login_required
def edit_employee(employee_id):
    with get_db() as db:
        employee = db.execute("SELECT * FROM employees WHERE id = ?", (employee_id,)).fetchone()
    if employee is None:
        flash("Employee not found.", "error")
        return redirect(url_for("index"))
    data = employee_form_data() if request.method == "POST" else dict(employee)
    if request.method == "POST":
        error = validate_employee(data)
        if error:
            flash(error, "error")
        else:
            try:
                with get_db() as db:
                    db.execute("UPDATE employees SET name = ?, email = ?, department = ?, job_title = ? WHERE id = ?",
                               (data["name"], data["email"].lower(), data["department"], data["job_title"], employee_id))
                flash("Employee updated.", "success")
                return redirect(url_for("index"))
            except sqlite3.IntegrityError:
                flash("Another employee already uses that email.", "error")
    return render_template("employee_form.html", employee=data, page_title="Edit employee", submit_label="Save changes")


@app.post("/employees/<int:employee_id>/delete")
@login_required
def delete_employee(employee_id):
    with get_db() as db:
        cursor = db.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    flash("Employee deleted." if cursor.rowcount else "Employee not found.", "success")
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
