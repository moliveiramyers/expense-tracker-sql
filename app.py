from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = "database.db"


# =========================
# DATABASE CONNECTION
# =========================
def connect():
    return sqlite3.connect(DB_NAME)


# =========================
# CREATE TABLES (NORMALIZED DB)
# =========================
def create_table():
    conn = connect()
    cur = conn.cursor()

    # TABLE 1: categories (lookup table)
    # WHY: avoids repeating category text in every expense
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    # TABLE 2: expenses (main table)
    # category_id is a FOREIGN KEY (relational database concept)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category_id INTEGER,
        date TEXT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    """)

    # DEFAULT DATA (seed categories)
    # WHY: ensures dropdown always has values even on fresh DB
    categories = [
        ("Groceries",),
        ("House Bills",),
        ("Restaurants",),
        ("Transport",),
        ("Rent",),
        ("Education",),
        ("Shopping",),
        ("Leisure",),
        ("Health",),
        ("Other",)
    ]

    cur.executemany("""
    INSERT OR IGNORE INTO categories(name)
    VALUES (?)
    """, categories)

    conn.commit()
    conn.close()


# =========================
# DASHBOARD / READ DATA
# =========================
@app.route("/")
def index():
    conn = connect()
    cur = conn.cursor()

    # =========================
    # FILTER BY MONTH (optional)
    # =========================
    month = request.args.get("month")

    # =========================
    # IMPORTANT FIX:
    # We now JOIN categories table so we can display
    # category NAME instead of category_id
    # =========================
    base_query = """
        SELECT 
            expenses.id,
            expenses.title,
            expenses.amount,
            categories.name AS category_name,
            expenses.date
        FROM expenses
        LEFT JOIN categories
            ON expenses.category_id = categories.id
    """

    # Apply filter if month exists
    if month:
        cur.execute(
            base_query + """
            WHERE strftime('%Y-%m', expenses.date) = ?
            ORDER BY expenses.date DESC
            """,
            (month,)
        )
    else:
        cur.execute(
            base_query + """
            ORDER BY expenses.date DESC
            """
        )

    expenses = cur.fetchall()

    # =========================
    # AGGREGATE FUNCTIONS
    # =========================

    # TOTAL SPENT
    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0] or 0

    # TOTAL TRANSACTIONS
    cur.execute("SELECT COUNT(*) FROM expenses")
    count = cur.fetchone()[0] or 0

    # BIGGEST EXPENSE
    cur.execute("SELECT MAX(amount) FROM expenses")
    max_expense = cur.fetchone()[0] or 0

    # GET ALL CATEGORIES (para dropdown e update)
    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()

    # MOST USED CATEGORY (NOW USING JOIN)
    cur.execute("""
        SELECT categories.name, COUNT(*) as c
        FROM expenses
        JOIN categories 
            ON expenses.category_id = categories.id
        GROUP BY categories.name
        ORDER BY c DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    top_category = row[0] if row else "N/A"

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        categories=categories,
        total=total,
        count=count,
        max_expense=max_expense,
        top_category=top_category,
        month=month
    )

# =========================
# CREATE EXPENSE
# =========================
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    amount = request.form["amount"]
    category_id = request.form["category_id"]
    date = request.form["date"]

    conn = connect()
    cur = conn.cursor()


    
    # CONVERT CATEGORY NAME → CATEGORY ID
    # WHY: relational database requirement
    cur.execute("SELECT id FROM categories WHERE name = ?", (category_id,))
    row = cur.fetchone()

    # SAFETY CHECK (avoid crash if category not found)
    category_id = row[0] if row else None

    # INSERT EXPENSE USING FOREIGN KEY
    cur.execute("""
    INSERT INTO expenses(title, amount, category_id, date)
    VALUES (?, ?, ?, ?)
    """, (title, amount, category_id, date))

    conn.commit()
    conn.close()

    return redirect("/")


# =========================
# DELETE EXPENSE
# =========================
@app.route("/delete/<int:id>")
def delete(id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM expenses WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


# =========================
# UPDATE EXPENSE (AJAX)
# =========================
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    data = request.get_json()

    conn = connect()
    cur = conn.cursor()

    # FIX:
    # frontend sends category NAME → we must convert to ID again
    cur.execute("SELECT id FROM categories WHERE name = ?", (data["category"],))
    row = cur.fetchone()
    category_id = row[0] if row else None

    cur.execute("""
    UPDATE expenses
    SET title = ?, amount = ?, category_id = ?, date = ?
    WHERE id = ?
    """, (
        data["title"],
        data["amount"],
        category_id,
        data["date"],
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "ok",
        "updated": id
    })


# =========================
# START APP
# =========================
if __name__ == "__main__":
    create_table()
    app.run(debug=True)