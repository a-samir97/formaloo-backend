# Generated by Django 5.0.1 on 2024-01-19 17:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("appstore", "0003_rename_unique_key_application_key_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="purchasedapplication",
            unique_together={("app", "user")},
        ),
    ]
