# Generated by Django 3.2 on 2021-11-14 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0011_orders_total_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="comments",
            name="rate",
            field=models.CharField(
                blank=True,
                choices=[
                    ("0", "0"),
                    ("1", "1"),
                    ("2", "2"),
                    ("3", "3"),
                    ("4", "4"),
                    ("5", "5"),
                ],
                default="0",
                max_length=100,
                null=True,
            ),
        ),
    ]
