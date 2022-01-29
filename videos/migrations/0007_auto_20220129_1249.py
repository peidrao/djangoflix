# Generated by Django 3.2.11 on 2022-01-29 12:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_video_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='published_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 1, 29, 12, 49, 50, 42152, tzinfo=utc)),
            preserve_default=False,
        ),
    ]