# Generated by Django 5.0.3 on 2024-07-17 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='local',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
