# Generated by Django 2.2.1 on 2019-08-13 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("rasa_api", "0007_auto_20190812_1924")]

    operations = [
        migrations.AddField(
            model_name="utteranceresponse",
            name="custom_json",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="utteranceresponse",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="utteranceresponse",
            name="text",
            field=models.TextField(blank=True, null=True),
        ),
    ]
