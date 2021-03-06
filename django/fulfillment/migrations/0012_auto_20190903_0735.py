# Generated by Django 2.2.4 on 2019-09-03 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("fulfillment", "0011_unlockform")]

    operations = [
        migrations.AddField(
            model_name="unlockform",
            name="network_name",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="unlockform",
            name="email",
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
