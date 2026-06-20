import json
import os
import smtplib
import uuid
from datetime import datetime
from email.mime.text import MIMEText

import functions_framework
from google.cloud import firestore

db = firestore.Client()

GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')


def send_confirmation_email(to_email, name, msg_id):
    """Send a contact-form confirmation email via Gmail SMTP.
    Failure to send email never blocks the message from being recorded.
    """
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("Email not sent: GMAIL_USER/GMAIL_APP_PASSWORD not configured.")
        return False

    subject = "We've received your message — ELEMENTS"
    body = (
        f"Hi {name},\n\n"
        f"Thanks for reaching out to ELEMENTS. We've received your message "
        f"(reference: {msg_id}) and will get back to you shortly.\n\n"
        f"Warm regards,\nELEMENTS"
    )

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False


@functions_framework.http
def handle_contact(request):
    """HTTP Cloud Function that receives a message from the ELEMENTS
    contact form, stores it in Firestore, sends a confirmation email,
    and returns a JSON success response.
    """
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    data = request.get_json(silent=True) or {}
    msg_id = f"MSG-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"

    contact = {
        'id': msg_id,
        'name': data.get('name'),
        'email': data.get('email'),
        'subject': data.get('subject'),
        'message': data.get('message'),
        'timestamp': datetime.now().isoformat()
    }

    try:
        db.collection('messages').document(msg_id).set(contact)
        print(f"Message saved to Firestore: {contact}")
    except Exception as e:
        print(f"Firestore write failed: {e}")
        return (
            json.dumps({
                'status': 'error',
                'message': 'Could not save your message. Please try again.'
            }),
            500,
            headers
        )

    email_sent = send_confirmation_email(
        contact['email'], contact['name'], msg_id
    )

    return (
        json.dumps({
            'status': 'success',
            'message': f"Thanks {contact['name']}! Your message has been received. Reference #{msg_id}",
            'email_sent': email_sent
        }),
        200,
        headers
    )
