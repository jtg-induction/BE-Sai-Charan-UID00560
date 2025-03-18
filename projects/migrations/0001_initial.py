# Generated by Django 5.1.7 on 2025-03-13 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("name", models.CharField(max_length=50)),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "To Be Started"),
                            (1, "In Progress"),
                            (2, "Completed"),
                        ],
                        default=0,
                    ),
                ),
                ("max_members", models.PositiveIntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectMember",
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
            ],
            options={
                "abstract": False,
            },
        ),
    ]
