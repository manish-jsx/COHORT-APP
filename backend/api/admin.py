from django.contrib import admin
from .models import CustomUser, Course, Module, Notebook, Video, UserProgress


admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Notebook)
admin.site.register(Video)
admin.site.register(UserProgress)
