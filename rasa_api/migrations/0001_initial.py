# Generated by Django 2.2.1 on 2019-08-01 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Utterance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UtteranceResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('utterance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rasa_api.Utterance')),
            ],
        ),
        migrations.CreateModel(
            name='UtteranceButton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('payload', models.CharField(max_length=255)),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rasa_api.UtteranceResponse')),
            ],
        ),
    ]
