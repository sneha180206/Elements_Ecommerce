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


def send_confirmation_email(to_email, name, product, order_id):
    """Send an order confirmation email via Gmail SMTP.
    Failure to send email never blocks the order from succeeding.
    """
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("Email not sent: GMAIL_USER/GMAIL_APP_PASSWORD not configured.")
        return False

    subject = "Your ELEMENTS Order Confirmation"
    body = (
        f"Hi {name},\n\n"
        f"Thank you for your order!\n\n"
        f"Order ID: {order_id}\n"
        f"Product: {product}\n\n"
        f"We will reach out shortly with delivery details.\n\n"
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
def handle_order(request):
    """HTTP Cloud Function that receives an order from the ELEMENTS
    storefront order form, stores it in Firestore, sends a confirmation
    email, and returns a JSON success response.
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
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"

    order = {
        'id': order_id,
        'name': data.get('name'),
        'email': data.get('email'),
        'product': data.get('product'),
        'status': 'received',
        'timestamp': datetime.now().isoformat()
    }

    # Persist to Firestore. If this fails, we still want the customer to
    # see a clear error rather than a false success.
    try:
        db.collection('orders').document(order_id).set(order)
        print(f"Order saved to Firestore: {order}")
    except Exception as e:
        print(f"Firestore write failed: {e}")
        return (
            json.dumps({
                'status': 'error',
                'message': 'Could not save your order. Please try again.'
            }),
            500,
            headers
        )

    email_sent = send_confirmation_email(
        order['email'], order['name'], order['product'], order_id
    )

    return (
        json.dumps({
            'status': 'success',
            'message': f"Order placed for {order['product']}! Confirmation #{order_id}",
            'email_sent': email_sent
        }),
        200,
        headers
    )
