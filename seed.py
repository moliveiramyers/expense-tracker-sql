import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()


# =========================
# RAW DATA (SEM IDs FIXOS)
# =========================
data = [
    ("Groceries Lidl", 25.50, "Groceries", "2026-01-05"),
    ("Rent January", 800, "Rent", "2026-01-01"),
    ("Uber ride", 12.30, "Transport", "2026-01-12"),

    ("Groceries Aldi", 40.10, "Groceries", "2026-02-03"),
    ("Electricity bill", 60.00, "House Bills", "2026-02-10"),
    ("Netflix", 12.99, "Other", "2026-02-15"),

    ("Restaurant dinner", 35.00, "Restaurants", "2026-03-08"),
    ("Train ticket", 18.50, "Transport", "2026-03-12"),
    ("Books", 22.00, "Education", "2026-03-20"),

    ("Shopping clothes", 120.00, "Shopping", "2026-04-02"),
    ("Gym", 30.00, "Health", "2026-04-10"),
    ("Groceries", 33.20, "Groceries", "2026-04-18"),
]


# =========================
# INSERT SAFE (CATEGORY NAME → ID)
# =========================
for title, amount, category_name, date in data:

    # convert category name into id
    cur.execute("""
        SELECT id FROM categories WHERE name = ?
    """, (category_name,))

    row = cur.fetchone()

    if row:
        category_id = row[0]
    else:
        category_id = None  # fallback safety

    # insert expense
    cur.execute("""
        INSERT INTO expenses (title, amount, category_id, date)
        VALUES (?, ?, ?, ?)
    """, (title, amount, category_id, date))


conn.commit()
conn.close()

print("Database seeded successfully (safe version)!")