import sqlite3

# Connect to the SQLite database
# Returns the database connection object

def connect_DB():
    db_name = "tasks.db"
    try:
        conn = sqlite3.connect(db_name)
        print("Database connection successful.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Create necessary tables: tasks and contacts
def create_Tables(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT DEFAULT 'normal',
            status TEXT DEFAULT 'pending'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            task_id INTEGER,
            email TEXT,
            phone TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks (task_id)
        )
    """)
    db.commit()
    print("Tables created or already exist.")

# Store or modify entries in the tasks table
def store_Entry(db, action, task_id=None, name=None, description=None, due_date=None, priority=None, status=None):
    cursor = db.cursor()
    if action in ["insert", "create"]:
        cursor.execute("""
            INSERT INTO tasks (name, description, due_date, priority, status)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, due_date, priority or 'normal', status or 'pending'))
        db.commit()
        print("Task inserted successfully with ID:", cursor.lastrowid)
        return cursor.lastrowid  # Return task_id of the inserted task
    elif action == "update" and task_id is not None:
        cursor.execute("""
            UPDATE tasks
            SET name = ?, description = ?, due_date = ?, priority = ?, status = ?
            WHERE task_id = ?
        """, (name, description, due_date, priority, status, task_id))
        print("Task updated.")
        db.commit()
    elif action == "delete" and task_id is not None:
        cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
        print("Task deleted.")
        db.commit()
    else:
        print("Invalid action or missing task_id.")

# Return task entries with optional filters for priority and status
def return_Entry(db, priority=None, status=None):
    cursor = db.cursor()
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if status:
        query += " AND status = ?"
        params.append(status)
    cursor.execute(query, params)
    return cursor.fetchall()

# Store or update a contact entry
def store_Contact(db, task_id, email, phone):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts WHERE task_id = ?", (task_id,))
    if cursor.fetchone():
        cursor.execute("""
            UPDATE contacts SET email = ?, phone = ? WHERE task_id = ?
        """, (email, phone, task_id))
        print("Contact info updated.")
    else:
        cursor.execute("""
            INSERT INTO contacts (task_id, email, phone)
            VALUES (?, ?, ?)
        """, (task_id, email, phone))
        print("Contact info added.")
    db.commit()

# Get the total number of tasks
def total_Tasks(db):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    print("Total task count from DB:", count)
    return count