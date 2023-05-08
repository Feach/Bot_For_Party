# Generated by Django 4.1.7 on 2023-05-08 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_statisticusercreate_statisticpartycreate'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticUserDelete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_user', models.CharField(default='Пользователь', max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=50)),
                ('discription', models.TextField(max_length=500)),
                ('user_id', models.CharField(max_length=50)),
                ('inside_id', models.CharField(max_length=50)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Статистика удаленных пользователей',
                'verbose_name_plural': 'Статистика удаленных пользователей',
            },
        ),
        migrations.AlterModelOptions(
            name='party',
            options={'verbose_name': 'Пати', 'verbose_name_plural': 'Пати'},
        ),
        migrations.AlterModelOptions(
            name='statisticpartycreate',
            options={'verbose_name': 'Статистика созданных пати', 'verbose_name_plural': 'Статистика созданных пати'},
        ),
        migrations.AlterModelOptions(
            name='statisticusercreate',
            options={'verbose_name': 'Статистика созданных пользователей', 'verbose_name_plural': 'Статистика созданных пользователей'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.CreateModel(
            name='StatisticPartyDelete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=50)),
                ('discription', models.TextField(max_length=500)),
                ('user_now', models.CharField(max_length=10)),
                ('user_max', models.CharField(max_length=10)),
                ('leader_id', models.CharField(max_length=50)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('users', models.ManyToManyField(blank=True, null=True, to='database.user')),
            ],
            options={
                'verbose_name': 'Статистика удаленных пати',
                'verbose_name_plural': 'Статистика удаленных пати',
            },
        ),
    ]