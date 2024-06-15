from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Sends a test email using Gmail.'

    def handle(self, *args, **options):
        try:
            send_mail(
                'Subject here',
                'Here is the message.',
                'manish.jsx@gmail.com',  
                ['manish.amhs@gmail.com'],  
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Test email sent successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending email: {e}'))
