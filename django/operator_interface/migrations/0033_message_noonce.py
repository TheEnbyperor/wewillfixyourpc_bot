# Generated by Django 2.2.4 on 2019-09-01 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("operator_interface", "0032_message_request_name")]

    operations = [
        migrations.AddField(
            model_name="message",
            name="noonce",
            field=models.CharField(blank=True, max_length=255, null=True),
        )
    ]
