# Generated by Django 4.2.6 on 2023-11-11 02:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workout_users", "0018_alter_post_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_pic",
            field=models.ImageField(max_length=10000, upload_to=""),
        ),
    ]