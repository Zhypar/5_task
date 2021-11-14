# Generated by Django 3.2 on 2021-11-12 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0008_alter_user_is_supplier"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="supplier",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"is_supplier": True},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]