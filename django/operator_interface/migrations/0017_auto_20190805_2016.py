# Generated by Django 2.2.1 on 2019-08-05 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operator_interface', '0016_auto_20190804_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.FilePathField(blank=True, null=True),
        ),
    ]