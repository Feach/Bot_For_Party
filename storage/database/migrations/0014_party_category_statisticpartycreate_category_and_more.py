# Generated by Django 4.1.7 on 2023-05-08 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_statisticuserdelete_alter_party_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='category',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='statisticpartycreate',
            name='category',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='statisticpartydelete',
            name='category',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
    ]
