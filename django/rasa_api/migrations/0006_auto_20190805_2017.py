# Generated by Django 2.2.1 on 2019-08-05 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("rasa_api", "0005_auto_20190805_2016")]

    operations = [
        migrations.RenameField(
            model_name="testinguser", old_name="sender_id", new_name="platform_id"
        )
    ]
