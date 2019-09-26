# Generated by Django 2.2.1 on 2019-09-24 20:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("keycloak_auth", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel("remoteuseropenidconnectprofile"),
        migrations.CreateModel(
            name="RemoteUserOpenIdConnectProfile",
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
                ("access_token", models.TextField(null=True)),
                ("expires_before", models.DateTimeField(null=True)),
                ("refresh_token", models.TextField(null=True)),
                ("refresh_expires_before", models.DateTimeField(null=True)),
                ("sub", models.CharField(max_length=255, unique=True)),
                (
                    "user",
                    models.OneToOneField(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="oidc_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]