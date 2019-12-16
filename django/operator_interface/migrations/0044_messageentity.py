# Generated by Django 2.2.5 on 2019-11-07 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operator_interface', '0043_auto_20191107_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operator_interface.Message')),
            ],
        ),
    ]