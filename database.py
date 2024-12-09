from PyQt6.QtSql import QSqlDatabase, QSqlQuery


# Helper function to log query execution details
def log_query_execution(query, bound_values):
    print("Executing Query:", query.executedQuery())  # Log the executed query
    print("Bound Parameters:", bound_values)  # Log the values bound to the query
    print("Query Error (if any):", query.lastError().text())  # Log any query error


# Initialize the database
def init_db(db_name):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
        return False

    query = QSqlQuery()
    query.exec("""
               CREATE TABLE IF NOT EXISTS expenses (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT,
                   category TEXT,
                   amount REAL,
                   description TEXT   
               )
               """)

    return True


# Fetch expenses from the database
def fetch_expenses():
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []
    while query.next():
        expenses.append([query.value(i) for i in range(5)])
    return expenses


# Add expense with debug logging
def add_expenses(date, category, amount, description):
    query = QSqlQuery()
    query.prepare("""
                  INSERT INTO expenses (date, category, amount, description)
                  VALUES (?, ?, ?, ?)
                  """)
    bound_values = [date, category, amount, description]  # Store bound values for debugging
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    if not query.exec():
        log_query_execution(query, bound_values)  # Log the query details on error
        return False

    return True


# Delete expense with debug logging
def delete_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    bound_values = [expense_id]  # Store bound values for debugging
    query.addBindValue(expense_id)

    if not query.exec():
        log_query_execution(query, bound_values)  # Log the query details on error
        return False

    return True


