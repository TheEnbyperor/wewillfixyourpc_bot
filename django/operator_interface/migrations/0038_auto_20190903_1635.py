# Generated by Django 2.2.4 on 2019-09-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("operator_interface", "0037_message_form_link")]

    operations = [
        migrations.RemoveField(model_name="message", name="form_link"),
        migrations.AddField(
            model_name="message",
            name="card",
            field=models.TextField(blank=True, null=True),
        ),
    ]