# Generated by Django 5.0.1 on 2024-01-11 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profilePicture/24/01/11/default.jpeg', upload_to='profilePicture/%y/%m/%d'),
        ),
    ]