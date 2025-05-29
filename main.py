from DatabaseManager import connect_DB, create_Tables, store_Entry, total_Tasks, store_Contact
from ErrorHandler import trigger_Check
from EventHandler import createEvent
from NotificationManager import send_Email, send_Message, push_Notifications

# Main user interaction menu
def menu():
    while True:
        print("\nEvent Alert System Menu")
        print("1. Add New Event")
        print("2. Add Contact to Task")
        print("3. Show Total Tasks")
        print("4. Run Trigger Check")
        print("5. Send Notifications Now")
        print("6. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            name = input("Enter event name: ")
            date = input("Enter date (YYYY-MM-DD): ")
            time_ = input("Enter time (HH:MM): ")
            task_id = createEvent(name, date, time_)
            print("Event created with task ID:", task_id)
        elif choice == "2":
            task_id = int(input("Enter task ID to add contact to: "))
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            db = connect_DB()
            store_Contact(db, task_id, email, phone)
            db.close()
            print("Contact added.")
        elif choice == "3":
            db = connect_DB()
            print("Total tasks:", total_Tasks(db))
            db.close()
        elif choice == "4":
            print("Checking triggers...")
            trigger_Check()
        elif choice == "5":
            email = input("Enter email: ")
            subject = input("Enter subject: ")
            body = input("Enter body: ")
            phone = input("Enter phone: ")
            message = input("Enter SMS message: ")
            notification = input("Enter push notification message: ")
            send_Email(email, subject, body)
            send_Message(phone, message)
            push_Notifications(notification)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

# Initialize DB and run menu
if __name__ == "__main__":
    db = connect_DB()
    create_Tables(db)
    db.close()
    menu()