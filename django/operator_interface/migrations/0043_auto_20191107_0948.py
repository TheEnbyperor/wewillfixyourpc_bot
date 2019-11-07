# Generated by Django 2.2.5 on 2019-11-07 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operator_interface', '0042_message_selection'),
    ]

    operations = [
        migrations.RemoveField(model_name='message', name='payment_confirm_id'),
        migrations.RemoveField(model_name='message', name='payment_request_id'),
        migrations.AddField(
            model_name='message',
            name='payment_confirm',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='payment_request',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
