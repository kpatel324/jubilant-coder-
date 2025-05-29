from ErrorHandler import logError

# Send email notifications
def send_Email(email, subject, body):
    try:
        print("Sending Email to:", email)
        print("Subject:", subject)
        print("Body:", body)
    except Exception as e:
        logError(str(e))

# Send SMS notifications
def send_Message(phone, message):
    try:
        print("Sending SMS to:", phone)
        print("Message:", message)
    except Exception as e:
        logError(str(e))

# Send push notifications
def push_Notifications(message):
    try:
        print("Push Notification:", message)
    except Exception as e:
        logError(str(e))