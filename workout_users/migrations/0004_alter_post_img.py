# Generated by Django 4.2.4 on 2023-10-10 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "workout_users",
            "0003_post_remove_workout_exercises_remove_user_height_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="img",
            field=models.URLField(max_length=10000),
        ),
    ]
