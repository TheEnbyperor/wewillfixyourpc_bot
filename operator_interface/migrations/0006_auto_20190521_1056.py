# Generated by Django 2.2.1 on 2019-05-21 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operator_interface', '0005_conversation_customer_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='customer_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
