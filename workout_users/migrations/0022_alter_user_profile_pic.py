# Generated by Django 4.2.6 on 2023-11-15 22:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workout_users", "0021_alter_user_profile_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_pic",
            field=models.ImageField(
                default="workout_users\\default-pfp.jpg", max_length=10000, upload_to=""
            ),
        ),
    ]