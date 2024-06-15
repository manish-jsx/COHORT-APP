from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User  # For user-related actions

from .models import Course, Module, Notebook, Video, CustomUser
from .serializers import CourseSerializer, ModuleSerializer, NotebookSerializer, VideoSerializer, UserSerializer, UserProgressSerializer
from django.contrib.auth import get_user_model
User = get_user_model()  # Get the currently active User model
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Allow anyone to view, but only authenticated users to modify

    # Optional: Add extra actions for course-related tasks
    @action(detail=True, methods=['get'])
    def enrolled_users(self, request, pk=None):
        course = self.get_object()
        enrolled_users = User.objects.filter(  # Assuming a ManyToMany relationship between User and Course
            courses_enrolled=course  # Replace with your actual field name
        )
        serializer = UserSerializer(enrolled_users, many=True)
        return Response(serializer.data)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access modules


class NotebookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notebook.objects.all()
    serializer_class = NotebookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Protect notebook access


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Protect video access


class UserViewSet(viewsets.ReadOnlyModelViewSet):  
    """Provides actions to list all users or retrieve a specific user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to register

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()  # Use the fetched User model
    serializer_class = UserSerializer
# ... (UserProgressViewSet if you have a UserProgress model)
