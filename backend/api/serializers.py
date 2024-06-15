from rest_framework import serializers
from .models import CustomUser, Course, Module, Notebook, Video, UserProgress
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}  # Hide password in responses
class EmailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Use get_user_model() to be flexible
        fields = ['first_name', 'last_name', 'email']  # Add fields you need in the email

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'url']


class NotebookSerializer(serializers.ModelSerializer):
    # Adding a URL field to directly access the notebook file
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Notebook
        fields = ['id', 'title', 'file_url']  # Note: Not including 'file' directly for security

    def get_file_url(self, obj):
        return obj.file.url if obj.file else None


class ModuleSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    notebooks = NotebookSerializer(many=True, read_only=True)
    # Adding a 'progress' field for user-specific progress (if applicable)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'title', 'content', 'videos', 'notebooks', 'progress']
    
    def get_progress(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                progress = UserProgress.objects.get(user=user, module=obj)
                return UserProgressSerializer(progress).data
            except UserProgress.DoesNotExist:
                return None
        return None


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'modules']


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'module', 'completed']  # Include relevant fields
