# Generated by Django 4.1.2 on 2022-10-15 10:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SpotifyToken",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("access_token", models.CharField(max_length=255)),
                ("token_type", models.CharField(max_length=255)),
                ("expires_in", models.IntegerField()),
                ("expires_at", models.IntegerField()),
                ("scope", models.TextField()),
                ("refresh_token", models.CharField(max_length=255)),
            ],
        ),
    ]
