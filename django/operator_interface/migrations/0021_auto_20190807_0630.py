# Generated by Django 2.2.1 on 2019-08-07 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("operator_interface", "0020_auto_20190807_0621")]

    operations = [
        migrations.RemoveField(model_name="paymentmessage", name="message"),
        migrations.AddField(
            model_name="message",
            name="payment_confirm_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="message",
            name="payment_request_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(name="PaymentConfirmMessage"),
        migrations.DeleteModel(name="PaymentMessage"),
    ]
