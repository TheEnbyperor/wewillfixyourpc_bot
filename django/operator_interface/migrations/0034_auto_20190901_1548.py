# Generated by Django 2.2.4 on 2019-09-01 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("operator_interface", "0033_message_noonce")]

    operations = [
        migrations.RemoveField(model_name="message", name="noonce"),
        migrations.AddField(
            model_name="conversation",
            name="noonce",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
