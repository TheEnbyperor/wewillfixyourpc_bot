# Generated by Django 2.2.1 on 2019-09-24 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("operator_interface", "0038_auto_20190903_1635")]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="customer_user_id",
            field=models.UUIDField(blank=True, null=True),
        )
    ]
