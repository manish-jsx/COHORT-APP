# #backend/views.py

# from django.conf import settings

# from django.contrib.auth import get_user_model
# from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
# from django.db import transaction
# from django.dispatch import receiver
# from django.utils.translation import gettext_lazy as _  # Use gettext_lazy instead of ugettext_lazy

# from allauth.account.signals import user_signed_up, email_confirmed, password_reset
# from allauth.account.adapter import get_adapter
# from allauth.utils import build_absolute_uri
# from django.contrib.auth.models import update_last_login 
# from dj_rest_auth.registration.views import RegisterView
# from dj_rest_auth.views import LoginView
# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from django.urls import reverse
# from .serializers import UserSerializer, CustomRegisterSerializer, EmailUserSerializer
# from .utils import send_email_from_template, logger
# from api.models import CustomUser
# from api.tasks import send_email_task
# from allauth.account.models import EmailAddress   # For email verification
# from .utils import get_absolute_url

# User = get_user_model()





# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.validated_data['user']
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 'token': token.key,
#                 'user_id': user.pk,
#                 'username': user.username,
#                 'email': user.email
#             })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]
#     http_method_names = ['get', 'post', 'head', 'options']


# class CustomRegisterView(RegisterView):
#     serializer_class = CustomRegisterSerializer

#     def get_response_data(self, user):
#         return {
#             'user_id': user.pk,
#             'username': user.username,
#             'email': user.email,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#         }

#      # Remove this function to disable the default behavior of returning a redirect response:
#     def get_email_confirmation_url(self, request, emailconfirmation):
#         """Constructs the email confirmation (activation) url."""
#         url = reverse("account_confirm_email", args=[emailconfirmation.key])
#         ret = build_absolute_uri(request, url, protocol=settings.DEFAULT_SITE_DOMAIN)  # This will construct the url using DEFAULT_SITE_DOMAIN setting
#         return ret
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.method == 'POST':
#             context['request'] = self.request
#         return context
    
#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)

#             # Create user using the serializer
#             user = serializer.save(request)

#             # Trigger email verification (if enabled)
#             if getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", None) == "mandatory":
#                 confirmation = EmailAddress.objects.filter(user=user).order_by('-id')[0]
#                 send_email_task.delay("activation", {
#                 'user': user.id,
#                 'confirmation_url': get_absolute_url(request, confirmation)
#                 })
#             else:
#                 # If email verification is not mandatory, log the user in directly
#                 self.perform_login(user)
            
#             return Response(self.get_response_data(user),
#                             status=status.HTTP_201_CREATED
#                         )
#         except Exception as e:
#             logger.error(f"Error registering user: {e} - Request: {request.data}")
#             return Response({"error": "An error occurred during registration."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def send_feedback_email(request):
#     try:
#         feedback_message = request.data.get('feedback_message')
#         if not feedback_message:
#             return Response({"error": "Feedback message is required."}, status=status.HTTP_400_BAD_REQUEST)
#         send_email_from_template(request.user, "feedback", {'feedback_message': feedback_message})
#         return Response({"message": "Feedback email sent successfully"}, status=status.HTTP_200_OK)
#     except Exception as e:
#         logger.error(f"Error sending feedback email: {e} - Request: {request.data}")
#         return Response({"error": "An error occurred while sending the feedback."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @receiver(user_signed_up)  # Signal for user registration
# def send_welcome_email(request, user, **kwargs):
#     send_email_task.delay("welcome", {'user': user})  



# @receiver(email_confirmed)
# def send_activation_email(request, email_address, **kwargs):
#     send_email_with_logging(email_address.user, "activation")



# @receiver(password_reset)
# def send_password_reset_email(request, user, **kwargs):
#     context = {
#         "user": user,
#         "email": user.email,
#         "request": request,
#     }
    
#     # This line is to ensure that the `password_reset_url` is present in the context
#     context["password_reset_url"] = get_adapter(
#         request
#     ).get_password_reset_url(request, user)

#     send_email_task.delay("password_reset", context)





# @receiver(user_logged_in)
# def user_logged_in_callback(sender, request, user, **kwargs):
#     logger.info(f"User logged in: {user.username}")
#     ip_address = request.META.get('REMOTE_ADDR')
#     user_agent = request.META.get('HTTP_USER_AGENT')
#     update_last_login(sender, user)
#     send_email_from_template(user, "login")


# @receiver(user_logged_out)
# def user_logged_out_callback(sender, request, user, **kwargs):
#     logger.info(f"User logged out: {user.username}")


# @receiver(user_login_failed)
# def user_login_failed_callback(sender, credentials, **kwargs):
#     logger.warning(f"User login failed: {credentials.get('username')}")




# def send_email_with_logging(user, email_type):
#     try:
#         send_email_from_template(user, email_type)
#     except Exception as e:
#         logger.error(f"Error sending {email_type} email: {e}")


# class CustomLoginView(LoginView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         user = self.request.user
#         send_email_with_logging(user, "login")
#         return response


# backend/views.py

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db import transaction
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from allauth.account.signals import user_signed_up, email_confirmed, password_reset
from allauth.utils import build_absolute_uri
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from allauth.account.models import EmailAddress

from .serializers import UserSerializer, CustomRegisterSerializer, EmailUserSerializer
from .utils import send_email_from_template, logger, get_absolute_url
from api.models import CustomUser
from api.tasks import send_email_task

User = get_user_model()


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'head', 'options']


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def get_response_data(self, user):
        return {
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url."""
        url = reverse("account_confirm_email", args=[emailconfirmation.key])
        return build_absolute_uri(request, url, protocol=settings.DEFAULT_SITE_DOMAIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['request'] = self.request
        return context

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Create user using the serializer
            user = serializer.save(request)

            # Serialize user data
            user_data = EmailUserSerializer(user).data

            # Trigger email verification (if enabled)
            if getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", None) == "mandatory":
                confirmation = EmailAddress.objects.filter(user=user).order_by('-id')[0]
                send_email_task.delay("activation", {
                    'user': user_data,
                    'confirmation_url': get_absolute_url(request, confirmation)
                })
            else:
                # If email verification is not mandatory, log the user in directly
                self.perform_login(user)

            return Response(self.get_response_data(user), status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error registering user: {e} - Request: {request.data}")
            return Response({"error": "An error occurred during registration."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_feedback_email(request):
    feedback_message = request.data.get('feedback_message')
    if not feedback_message:
        return Response({"error": "Feedback message is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        send_email_from_template(request.user, "feedback", {'feedback_message': feedback_message})
        return Response({"message": "Feedback email sent successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error sending feedback email: {e} - Request: {request.data}")
        return Response({"error": "An error occurred while sending the feedback."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    user_data = EmailUserSerializer(user).data  # Serialize user data
    send_email_task.delay("welcome", {'user': user_data})


@receiver(email_confirmed)
def send_activation_email(request, email_address, **kwargs):
    send_email_with_logging(email_address.user, "activation")


@receiver(password_reset)
def send_password_reset_email(request, user, **kwargs):
    context = {
        "user": EmailUserSerializer(user).data,  # Serialize user data
        "email": user.email,
        "request": request,
        "password_reset_url": get_adapter(request).get_password_reset_url(request, user)
    }
    send_email_task.delay("password_reset", context)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    logger.info(f"User logged in: {user.username}")
    update_last_login(sender, user)
    send_email_from_template(user, "login")


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    logger.info(f"User logged out: {user.username}")


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    logger.warning(f"User login failed: {credentials.get('username')}")


def send_email_with_logging(user, email_type):
    try:
        send_email_from_template(user, email_type)
    except Exception as e:
        logger.error(f"Error sending {email_type} email: {e}")


class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        send_email_with_logging(request.user, "login")
        return response
