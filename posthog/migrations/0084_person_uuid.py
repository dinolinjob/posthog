# Generated by Django 3.0.7 on 2020-09-21 14:00

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posthog", "0083_auto_20200826_1504"),
    ]

    operations = [
        migrations.AddField(
            model_name="person", name="uuid", field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]
