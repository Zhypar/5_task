# Generated by Django 3.2 on 2021-11-13 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0010_orders_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="orders",
            name="total_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
            preserve_default=False,
        ),
    ]
