# Generated by Django 2.2.4 on 2019-08-31 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("operator_interface", "0026_auto_20190816_0858")]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="noonce",
            field=models.CharField(blank=True, default="", max_length=255),
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
                    ("GA", "Actions on Google"),
                ],
                max_length=2,
            ),
        ),
    ]
