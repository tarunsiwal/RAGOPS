# Generated by Django 4.2.7 on 2023-11-28 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_uploadedfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='chathistory',
            name='prompt',
            field=models.TextField(blank=True),
        ),
    ]
