# Generated by Django 2.1.3 on 2019-06-15 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("operator_interface", "0011_notificationsubscription")]

    operations = [
        migrations.AlterModelOptions(
            name="message", options={"ordering": ("timestamp",)}
        )
    ]
