# Generated by Django 2.2.1 on 2019-08-03 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_paymenttoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=255),
        ),
    ]