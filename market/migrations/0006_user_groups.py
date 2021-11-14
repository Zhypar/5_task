# Generated by Django 3.2 on 2021-11-09 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("market", "0005_alter_user_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="market_groups",
                to="auth.group",
            ),
        ),
    ]
