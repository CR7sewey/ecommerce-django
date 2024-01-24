# Generated by Django 5.0.1 on 2024-01-24 13:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total", models.FloatField(verbose_name="Total")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("A", "Aprovado"),
                            ("C", "Criado"),
                            ("R", "Reprovado"),
                            ("P", "Pendente"),
                            ("E", "Enviado"),
                            ("F", "Finalizado"),
                        ],
                        default="C",
                        max_length=1,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_order",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.CreateModel(
            name="ItemOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product", models.CharField(max_length=255)),
                ("product_id", models.PositiveIntegerField()),
                ("variation", models.CharField(max_length=255)),
                ("variation_id", models.PositiveIntegerField()),
                ("price", models.FloatField()),
                ("promotion_price", models.FloatField(default=0)),
                ("quantity", models.PositiveIntegerField()),
                ("image", models.CharField(max_length=2000)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orders.order"
                    ),
                ),
            ],
            options={
                "verbose_name": "ItemOrder",
                "verbose_name_plural": "ItemOrders",
            },
        ),
    ]