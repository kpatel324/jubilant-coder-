from datetime import datetime, timedelta
from DatabaseManager import connect_DB, return_Entry, store_Entry, store_Contact
from NotificationManager import send_Email, send_Message, push_Notifications

# Create a new scheduled event if the date is valid
def createEvent(name, date, time_):
    try:
        due_date = date + " " + time_
        due_datetime = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        now = datetime.now()
        if due_datetime < now:
            print("Cannot create event in the past.")
            return
        db = connect_DB()
        task_id = store_Entry(db, "create", None, name, "Scheduled Event", due_date)
        db.close()
        return task_id
    except Exception as e:
        print("Error creating event:", e)
        return None

# Manually set trigger to notify if task is due within a specified time frame
def setTrigger(task_id, condition_minutes):
    try:
        db = connect_DB()
        tasks = return_Entry(db)
        for task in tasks:
            if task[0] == task_id:
                task_name = task[1]
                due_date_str = task[3]
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
                now = datetime.now()
                time_difference = due_date - now
                if timedelta(minutes=condition_minutes) >= time_difference > timedelta(0):
                    print(f"Task '{task_name}' is due in {condition_minutes} minutes!")
                    cursor = db.cursor()
                    cursor.execute("SELECT email, phone FROM contacts WHERE task_id = ?", (task_id,))
                    contact = cursor.fetchone()
                    if contact:
                        email, phone = contact
                        send_Email(email, "Reminder for task", f"Your task '{task_name}' is due soon!")
                        send_Message(phone, f"Reminder: {task_name} is due soon!")
                        push_Notifications(f"Reminder for: {task_name}")
        db.close()
    except Exception as e:
        print("Error in setting trigger:", e)