import json
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


def index(request):
    """Serve the main landing page."""
    return render(request, 'index.html')


@require_POST
def api_appointments(request):
    """Handle appointment form submissions via JSON POST."""
    try:
        data = json.loads(request.body)

        first_name = data.get('firstName', '').strip()
        last_name = data.get('lastName', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        service = data.get('service', '').strip()
        message = data.get('message', '').strip()

        # Basic validation
        if not all([first_name, last_name, email, phone]):
            return JsonResponse(
                {'error': 'Please fill in all required fields.'},
                status=400,
            )

        # Log the appointment
        logger.info(
            'New Appointment — Name: %s %s, Email: %s, Phone: %s, Service: %s',
            first_name, last_name, email, phone, service,
        )

        # Send email notification if SMTP is configured
        receiver_email = getattr(settings, 'RECEIVER_EMAIL', None)
        smtp_user = getattr(settings, 'EMAIL_HOST_USER', None)

        if smtp_user and receiver_email:
            try:
                subject = f'New Appointment Request: {first_name} {last_name}'
                text_body = (
                    f'You have received a new appointment request.\n\n'
                    f'Name: {first_name} {last_name}\n'
                    f'Email: {email}\n'
                    f'Phone: {phone}\n'
                    f'Service: {service}\n'
                    f'Message: {message or "None provided"}\n'
                )
                send_mail(
                    subject,
                    text_body,
                    f'"Orthocare Website" <{smtp_user}>',
                    [receiver_email],
                    fail_silently=False,
                )
                logger.info('Notification email sent successfully.')
            except Exception:
                logger.exception('Failed to send notification email.')
        else:
            logger.info('Skipping email notification: credentials not set in .env file.')

        return JsonResponse({
            'message': (
                'Appointment successfully requested! '
                'Our clinic will contact you shortly to confirm the scheduled time.'
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
