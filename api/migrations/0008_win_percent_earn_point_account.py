# Generated by Django 4.1.2 on 2023-12-17 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_usergame_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Win_Percent',
            fields=[
                ('percent', models.IntegerField()),
                ('pid', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Earn_Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('A', models.CharField(max_length=255)),
                ('B', models.CharField(max_length=255)),
                ('C', models.CharField(max_length=255)),
                ('D', models.CharField(max_length=255)),
                ('E', models.CharField(max_length=255)),
                ('F', models.CharField(max_length=255)),
                ('G', models.CharField(max_length=255)),
                ('H', models.CharField(max_length=255)),
                ('I', models.CharField(max_length=255)),
                ('J', models.CharField(max_length=255)),
                ('K', models.CharField(max_length=255)),
                ('L', models.CharField(max_length=255)),
                ('M', models.CharField(max_length=255)),
                ('N', models.CharField(max_length=255)),
                ('O', models.CharField(max_length=255)),
                ('P', models.CharField(max_length=255)),
                ('Q', models.CharField(max_length=255)),
                ('R', models.CharField(max_length=255)),
                ('S', models.CharField(max_length=255)),
                ('T', models.CharField(max_length=255)),
                ('earnpoint', models.IntegerField()),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.datemodel')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('play_points', models.IntegerField()),
                ('earn_points', models.IntegerField()),
                ('end_points', models.IntegerField()),
                ('profit', models.FloatField()),
                ('net_profit', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customuser')),
            ],
        ),
    ]
