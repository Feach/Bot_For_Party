# Generated by Django 4.1.7 on 2023-04-23 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_user_create_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='inside_id',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
    ]
