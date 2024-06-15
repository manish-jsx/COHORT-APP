# backend/utils.py
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from rest_framework.views import exception_handler
import smtplib
import logging


from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework that includes the HTTP status code in the response.
    """
    response = exception_handler(exc, context)

    # If response is not None, add the HTTP status code to the response
    if response is not None:
        response.data['status_code'] = response.status_code

    # Log the error
    logger.error(f"Error: {exc} - Request: {context['request'].data}")

    return response



def send_email_from_template(user, email_type, context={}):
    try:
        context['user'] = user
        html_content = render_to_string(f'account/email/{email_type}.html', context)
        text_content = render_to_string(f'account/email/{email_type}.txt', context)
        subject = render_to_string(f'account/email/{email_type}_subject.txt', context).strip()
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info(f"Sent {email_type} email to {user.email}")
    except TemplateDoesNotExist as e:
        logger.error(f"Template not found for {email_type}: {e}")
    except BadHeaderError as e:
        logger.error(f"Invalid header found in {email_type}: {e}")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error sending {email_type} email to {user.email}: {e}")


def get_absolute_url(request, confirmation):
    current_site = get_current_site(request)
    return confirmation.get_absolute_url(current_site.domain)
