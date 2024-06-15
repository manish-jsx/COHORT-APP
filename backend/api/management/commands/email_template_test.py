import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives,BadHeaderError
from django.template.exceptions import TemplateSyntaxError
from django.conf import settings
import smtplib
from datetime import datetime, timedelta
import logging
from backend.api.tasks import send_email_task
# Set up logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sends test emails from the account/email directory"

    def handle(self, *args, **options):
        template_dir = settings.BASE_DIR / 'templates' / 'account' / 'email'
        templates = [f for f in template_dir.glob('*.html') if f.name != 'email_base.html']

        for template_path in templates:  # Changed to template_path
            email_type = template_path.stem

            try:
                # Prepare context data based on email type
                context = {'user': {'first_name': 'Test User'}}
                if email_type == 'activation':
                    context['activate_url'] = 'https://www.example.com/activate'  # Replace with actual URL
                elif email_type == 'password_reset':
                    context['password_reset_url'] = 'https://www.example.com/reset-password'
                    context['password_reset_timeout'] = 24 
                elif email_type == 'subscription_confirmation':
                    context['subscription_plan'] = 'Premium'
                    context['subscription_amount'] = 99.99
                    context['subscription_renewal_date'] = datetime.now() + timedelta(days=30)
                elif email_type == 'billing_invoice':
                    context['due_date'] = datetime.now() + timedelta(days=15)
                    context['invoice_amount'] = 49.99
                    context['invoice_number'] = 'INV-12345'
                elif email_type == 'trial_expiration':
                    context['trial_end_date'] = datetime.now() + timedelta(days=3)
                elif email_type == 'feedback_survey':
                    context['survey_link'] = 'https://www.example.com/survey'
                elif email_type == 'security_alert':
                    context['alert_date'] = datetime.now()
                    context['ip_address'] = '192.168.1.100'
                elif email_type == 'support_help_desk':
                    context['ticket_number'] = 'TICKET-56789'
                    context['faq_link'] = 'https://www.example.com/faq'
                
                # Load templates and send email (same as before)
                html_content = render_to_string(str(template_path), context)
                text_content = render_to_string(template_dir / f'{email_type}.txt', context)


                # Create the email message
                subject = f'Test: {email_type.replace("_", " ").title()}'
                from_email = 'manish.jsx@gmail.com'  # Replace with your email
                to_email = ['manish.amhs@gmail.com']  # Replace with recipient email

                # Send the email
                msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                self.stdout.write(self.style.SUCCESS(f'Sent {email_type} email successfully!'))
            except FileNotFoundError as e:
                      self.stdout.write(self.style.ERROR(f'Template file not found for {email_type}: {e}'))
            except TemplateSyntaxError as e:
                      self.stdout.write(self.style.ERROR(f'Template syntax error in {email_type}: {e}'))
            except BadHeaderError as e:  # Catch invalid header errors (e.g., newlines in subject)
                      self.stdout.write(self.style.ERROR(f'BadHeaderError in {email_type}: {e}'))
            except smtplib.SMTPException as e:  # Catch general SMTP errors (connection issues, etc.)
                      self.stdout.write(self.style.ERROR(f'SMTP error in {email_type}: {e}'))
            except Exception as e:  # Catch all other exceptions
                      logger.exception(f'Unexpected error sending {email_type} email: {e}')  # Log with traceback
                      self.stdout.write(self.style.ERROR(f'Unexpected error sending {email_type} email. See logs for details.'))
