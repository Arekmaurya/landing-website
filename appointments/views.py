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
    """Handle appointment form submissions and email the admin."""
    try:
        data = json.loads(request.body)

        name = data.get('name', '').strip()
        age = data.get('age', '').strip()
        sex = data.get('sex', '').strip()
        contact = data.get('contact', '').strip()

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

        # Send email notification to admin
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
