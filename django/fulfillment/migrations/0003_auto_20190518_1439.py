# Generated by Django 2.1.3 on 2019-05-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("fulfillment", "0002_auto_20190518_1439")]

    operations = [
        migrations.AlterField(
            model_name="openinghoursoverride",
            name="close",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="openinghoursoverride",
            name="open",
            field=models.TimeField(blank=True, null=True),
        ),
    ]
