from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "database.db"

# Connect to Database
def connect():
    return sqlite3.connect(DB_NAME)


# Table Expense Tracker
def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        date TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = connect()
    cur = conn.cursor()

    # Filter by month
    month = request.args.get("month")
    if month:
        cur.execute("""
            SELECT * FROM expenses
            WHERE strftime('%Y-%m', date) = ?
            ORDER BY date DESC
        """, (month,))
    else:
        cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cur.fetchall()

    # TOTAL 
    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0] or 0

    # COUNT 
    cur.execute("SELECT COUNT(*) FROM expenses")
    count = cur.fetchone()[0]

    # MAX EXPENSE
    cur.execute("SELECT MAX(amount) FROM expenses")
    max_expense = cur.fetchone()[0] or 0

    # MOST USED CATEGORY
    cur.execute("""
    SELECT category, COUNT(*) as c
    FROM expenses
    GROUP BY category
    ORDER BY c DESC
    LIMIT 1
    """)
    row = cur.fetchone()
    top_category = row[0] if row else "N/A"

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        count=count,
        max_expense=max_expense,
        top_category=top_category,
        month=month
        )


@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]

    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
    INSERT INTO expenses(title, amount, category, date)
    VALUES (?, ?, ?, ?)
    """, (title, amount, category, date))

    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    data = request.get_json()

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE expenses
    SET title = ?, amount = ?, category = ?, date = ?
    WHERE id = ?
    """, (
        data["title"],
        data["amount"],
        data["category"],
        data["date"],
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
    "status": "ok",
    "updated": id
})
    

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
    
