# Generated by Django 2.2.1 on 2019-07-28 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fulfillment', '0007_auto_20190728_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneUnlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time', models.CharField(max_length=255)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fulfillment.Brand')),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fulfillment.Network')),
            ],
        ),
    ]