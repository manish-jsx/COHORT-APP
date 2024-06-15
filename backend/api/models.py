# from django.conf import settings
# from django.db import models
# from django.contrib.auth.models import User, AbstractUser 


# class CustomUser(AbstractUser):
#     # Default fields from AbstractUser: username, email, password, first_name, last_name, etc.
#     # Add your custom fields here (if needed):
#     phone_number = models.CharField(max_length=20, blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     # ... other custom fields ...

#     # You can override the USERNAME_FIELD if you want to use email for login:
#     # USERNAME_FIELD = 'email'

#     def __str__(self):
#         return self.username  # Or return self.email if using email as username

    


#     # Update the related_name attributes
#     groups = models.ManyToManyField(
#         'auth.Group', 
#         related_name='customuser_set', # Specify a unique related_name
#         blank=True, help_text='The groups this user belongs to.',
#         verbose_name='groups'
#     )

#     user_permissions = models.ManyToManyField(
#         'auth.Permission', 
#         related_name='customuser_set', # Specify a unique related_name
#         blank=True, help_text='Specific permissions for this user.',
#         verbose_name='user permissions'
#     )


# class Course(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     # Other fields like image, price, instructor, etc.
#     image = models.ImageField(upload_to='course_images/', blank=True, null=True)
#     instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_taught', blank=True, null=True)
#     price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     duration = models.CharField(max_length=50, blank=True, null=True) # E.g., '4 weeks', '3 months'
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title


# class Module(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     # Other fields like resources, order, etc.
#     order = models.PositiveIntegerField(default=0)  # Add an order field


#     def __str__(self):
#         return self.title


# class Notebook(models.Model):
#     module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='notebooks')  # Changed to allow multiple notebooks per module
#     title = models.CharField(max_length=255) # Added title for notebook
#     file = models.FileField(upload_to='notebooks/')
    

# class Video(models.Model):
#     module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
#     title = models.CharField(max_length=255)
#     url = models.URLField()

#     def __str__(self):
#         return self.title


# # Assuming you want to track user progress:
# class UserProgress(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     module = models.ForeignKey(Module, on_delete=models.CASCADE)
#     completed = models.BooleanField(default=False)
#     # ... other fields like quiz scores, notes, etc.
#     quiz_scores = models.JSONField(blank=True, null=True)  # Assuming you have quizzes
#     notes = models.TextField(blank=True, null=True)
#     last_accessed = models.DateTimeField(auto_now=True)


from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True, help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True, help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_taught', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Notebook(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='notebooks')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='notebooks/')

class Video(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    quiz_scores = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.module.title}'
