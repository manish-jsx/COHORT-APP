# Generated by Django 5.0.6 on 2024-06-15 03:52

from django.db import migrations, models

def handle_foreign_keys(apps, schema_editor):
    CustomUser = apps.get_model('api', 'CustomUser')
    
    # Example: Handling foreign keys issues, adjust according to your models
    for user in CustomUser.objects.all():
        # Example check: ensure user is linked properly
        if not user.is_active:  # Adjust condition as needed
            user.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.RunPython(handle_foreign_keys),

    ]
