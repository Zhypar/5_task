# Generated by Django 3.2 on 2021-11-13 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0009_alter_product_supplier"),
    ]

    operations = [
        migrations.AddField(
            model_name="orders",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("status-none", "None"), ("purchased", "Purchased")],
                default="status-none",
                max_length=100,
                null=True,
            ),
        ),
    ]
