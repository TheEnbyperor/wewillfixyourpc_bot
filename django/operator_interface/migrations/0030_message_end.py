# Generated by Django 2.2.4 on 2019-08-31 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operator_interface', '0029_remove_conversation_noonce'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='end',
            field=models.BooleanField(default=False),
        ),
    ]
