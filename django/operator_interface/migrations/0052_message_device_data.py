# Generated by Django 3.0.4 on 2020-03-23 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operator_interface', '0051_message_reaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='device_data',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]