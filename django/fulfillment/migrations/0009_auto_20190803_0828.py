# Generated by Django 2.2.1 on 2019-08-03 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("fulfillment", "0008_brand_network_phoneunlock")]

    operations = [
        migrations.AddField(
            model_name="brand",
            name="display_name",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="network",
            name="display_name",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="NetworkAlternativeName",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("display_name", models.CharField(max_length=255)),
                (
                    "network",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fulfillment.Network",
                    ),
                ),
            ],
        ),
    ]
