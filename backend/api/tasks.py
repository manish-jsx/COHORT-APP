# api/tasks.py

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from django.template.exceptions import TemplateDoesNotExist
import smtplib
import logging
from django.contrib.auth import get_user_model
from api.serializers import EmailUserSerializer
from api.models import CustomUser
User = get_user_model() 
# Logging
logger = logging.getLogger(__name__)

@shared_task
def send_email_task(email_type, context):
    try:
        user_serializer = EmailUserSerializer(data=context['user'])
        # if user_serializer.is_valid():
        user = user_serializer.save()
        html_content = render_to_string(f'account/email/{email_type}.html', {'user': user})  # Use the fetched user object
        text_content = render_to_string(f'account/email/{email_type}_message.txt', {'user': user})
        subject = render_to_string(f'account/email/{email_type}_subject.txt', {'user': user}).strip()
     


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
