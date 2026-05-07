from flask import Flask, render_template, request, redirect
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
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    conn.close()
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]

    conn = connect()
    cur = conn.cursor("""
    INSERT INTO expenses(title, amount, category, date)
    VALUES (?, ?, ?, ?)
    """, (title, amount, category, date))

@app.route("/delete/<int:id>")
def delete(id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
    

# # Insert data
# def add_expense(title, amount, category, date):
#     conn = connect()
#     cur = conn.cursor()

#     cur.execute("""
#     INSERT INTO expenses (title, amount, category, date)
#     VALUES (?,?,?,?)
#     """, (title, amount, category, date)
#     )
#     # save new changes
#     conn.commit()
#     conn.close()

# # SELECT 
# def list_expenses():
#     conn = connect()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM expenses")
#     rows = cur.fetchall()

#     conn.close()
#     return rows

# #  DELETE
# def delete_expense(expense_id, title, amout, category):
#     conn = connect()
#     cur = conn.cursor()

#     cur.execute(" DELETE FROM expenses WHERE id = ?", (expense_id))

#     conn.commit()
#     conn.close()

# # UPDATE
# def update_expense(expense_id, title, amount, category):
#     conn = connect()
#     cur = conn.cursor()

#     cur.execute("""
#     UPDATE expenses
#     SET title = ?, amount = ?, category = ?
#     WHERE id = ?
#     """)
#     conn.commit()
#     conn.close()

# # TEST 

# create_table()

# add_expense("Lunch", 12.5, "Food", "2026-05-07")
# add_expense("Bus ticket", 2.0, "Transport", "2026-05-07")

# print("EXPENSES: ")

# for e in list_expenses():
#     print(e)


# #delete_expense(1)
# #update_expense(2, "Bus ticket", 3.0, "Transport")