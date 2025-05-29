import logging
from datetime import datetime

# Configure logging to file
logging.basicConfig(filename="error.log", level=logging.ERROR)

# Log error messages with a timestamp
def logError(error_message):
    logging.error(str(datetime.now()) + ": " + error_message)

# Check upcoming tasks and trigger notifications if due soon
def trigger_Check():
    from DatabaseManager import connect_DB, return_Entry
    from NotificationManager import send_Email, send_Message, push_Notifications

    try:
        db = connect_DB()
        now = datetime.now()
        tasks = return_Entry(db)
        for task in tasks:
            task_id = task[0]
            name = task[1]
            due_date_str = task[3]
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
            time_difference = (due_date - now).total_seconds()
            if 0 <= time_difference < 600:
                cursor = db.cursor()
                cursor.execute("SELECT email, phone FROM contacts WHERE task_id = ?", (task_id,))
                contact = cursor.fetchone()
                if contact:
                    email, phone = contact
                    send_Email(email, "Reminder for task", f"Your task '{name}' is due soon!")
                    send_Message(phone, f"Reminder: {name} is due!")
                    push_Notifications(f"Reminder for: {name}")
                cursor.close()
        db.close()
    except Exception as e:
        logError(str(e))