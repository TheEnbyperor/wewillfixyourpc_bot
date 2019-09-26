# Generated by Django 2.2.1 on 2019-08-16 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("operator_interface", "0025_message_request_phone")]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="platform_from_id",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="conversation",
            name="platform",
            field=models.CharField(
                choices=[
                    ("FB", "Facebook"),
                    ("TW", "Twitter"),
                    ("TG", "Telegram"),
                    ("AZ", "Azure"),
                ],
                max_length=2,
            ),
        ),
    ]
