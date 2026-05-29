import json
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

import os
import requests
logger = logging.getLogger(__name__)


def index(request):
    """Serve the main landing page."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    credentials = []
    reviews = []
    
    try:
        with open(os.path.join(base_dir, 'data', 'credentials.json'), 'r') as f:
            credentials = json.load(f)
    except Exception as e:
        logger.error(f"Error loading credentials: {e}")

    try:
        with open(os.path.join(base_dir, 'data', 'reviews.json'), 'r') as f:
            reviews = json.load(f)
    except Exception as e:
        logger.error(f"Error loading reviews: {e}")
        
    context = {
        'credentials': credentials,
        'reviews': reviews,
    }
    return render(request, 'index.html', context)


@require_POST
def api_appointments(request):
    """Handle appointment form submissions and email the admin."""
    try:
        data = json.loads(request.body)

        name = str(data.get('name', '')).strip()
        age = str(data.get('age', '')).strip()
        sex = str(data.get('sex', '')).strip()
        contact = str(data.get('contact', '')).strip()

        # Basic validation
        if not all([name, age, sex, contact]):
            return JsonResponse(
                {'error': 'Please fill in all required fields.'},
                status=400,
            )

        # Log the appointment
        logger.info(
            'New Appointment — Name: %s, Age: %s, Sex: %s, Contact: %s',
            name, age, sex, contact,
        )

        # Determine notification method
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, 'data', 'config.json')
        notification_method = 'email'
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                notification_method = config.get('notification_method', 'email').lower()
        except Exception as e:
            logger.error(f"Error loading config.json: {e}")

        # Send Email Notification
        if notification_method in ['email', 'both']:
            receiver_email = getattr(settings, 'RECEIVER_EMAIL', None)
            smtp_user = getattr(settings, 'EMAIL_HOST_USER', None)

            if smtp_user and receiver_email:
                try:
                    subject = f'New Booking: {name}'
                    text_body = (
                        f'New appointment booking received.\n\n'
                        f'Name: {name}\n'
                        f'Age: {age}\n'
                        f'Sex: {sex}\n'
                        f'Contact: {contact}\n'
                    )
                    send_mail(
                        subject,
                        text_body,
                        f'"Orthocare Website" <{smtp_user}>',
                        [receiver_email],
                        fail_silently=False,
                    )
                    logger.info('Notification email sent to admin.')
                except Exception:
                    logger.exception('Failed to send notification email.')
            else:
                logger.warning(
                    'Email not sent: SMTP credentials not configured in .env'
                )

        # Send WhatsApp Notification
        if notification_method in ['whatsapp', 'both']:
            phone_number_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', None)
            access_token = getattr(settings, 'WHATSAPP_ACCESS_TOKEN', None)
            admin_whatsapp_number = getattr(settings, 'ADMIN_WHATSAPP_NUMBER', None)

            if phone_number_id and access_token and admin_whatsapp_number:
                url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "messaging_product": "whatsapp",
                    "to": admin_whatsapp_number,
                    "type": "text",
                    "text": {
                        "body": (
                            f"New appointment booking received.\n\n"
                            f"Name: {name}\n"
                            f"Age: {age}\n"
                            f"Sex: {sex}\n"
                            f"Contact: {contact}\n"
                        )
                    }
                }
                try:
                    response = requests.post(url, headers=headers, json=payload)
                    response.raise_for_status()
                    logger.info('WhatsApp notification sent to admin.')
                except Exception as e:
                    logger.exception(f'Failed to send WhatsApp notification: {e}')
            else:
                logger.warning('WhatsApp not sent: API credentials not configured in .env')

        return JsonResponse({
            'message': (
                'Booking confirmed! '
                'Our team will contact you shortly.'
            ),
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request body.'}, status=400)
    except Exception:
        logger.exception('Error handling appointment.')
        return JsonResponse(
            {'error': 'Internal server error. Please try again later.'},
            status=500,
        )
