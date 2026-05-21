# Overview

This project is a personal finance tracking web application built to improve my understanding of full-stack development and relational database integration. The system allows users to record, edit, delete, and analyze their daily expenses through a simple and interactive dashboard interface.

The application is built using Flask on the backend and integrates a SQLite relational database to persist financial records. Users can add expenses with details such as title, amount, category, and date. These records are stored in structured database tables and dynamically rendered on the frontend using Flask templates.

The system also includes real-time editing of expenses directly from the table interface, filtering by month, and a dashboard that summarizes key financial insights such as total spending, number of transactions, largest expense, and most used category.

The purpose of this project is to strengthen my skills in backend development, database design, and frontend integration while building a practical and usable financial tracking tool.

The database was improved by normalizing the structure into two related tables (expenses and categories) using foreign keys and SQL JOIN operations to ensure better data organization and consistency.

[Software Demo Video](http://youtube.link.goes.here)

---

# Relational Database

The application uses SQLite as the relational database engine. SQLite was chosen due to its simplicity and ease of integration with Python through the built-in `sqlite3` module.

The database contains a single table called `expenses`, which stores all financial records.

### Table structure:

**expenses**
- id (INTEGER, Primary Key, Auto Increment)
- title (TEXT) – description of the expense
- amount (REAL) – value of the expense
- category (TEXT) – classification such as food, transport, etc.
- date (TEXT) – date of the expense

This structure allows efficient storage and querying of financial data. SQL operations such as INSERT, UPDATE, DELETE, and SELECT are used throughout the application to manipulate and retrieve data dynamically.

---

# Development Environment

The project was developed using the following tools:

- Visual Studio Code
- Python 3.13
- Flask (web framework)
- SQLite (database engine)
- SQLite3 module (Python built-in)
- HTML, CSS, and JavaScript (frontend)
- DB Browser for SQLite (for database inspection and debugging)

The backend is written in Python using Flask, which handles routing and communication with the database. The frontend uses HTML templates with Jinja2 for dynamic rendering, CSS for styling, and JavaScript for asynchronous updates (fetch API).

---

# Useful Websites

- https://flask.palletsprojects.com/
- https://www.sqlite.org/docs.html
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Fetch_API
- https://jinja.palletsprojects.com/
- https://www.w3schools.com/sql/

---

# Future Work

- Add user authentication (login system)
- Improve mobile responsiveness of the dashboard
- Add data visualization charts (spending by category)
- Implement recurring expenses feature
- Improve validation and error handling
- Deploy the application online (Render or Railway)