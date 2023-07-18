# Generated by Django 4.2.3 on 2023-07-18 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MyBoard",
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
                ("myname", models.CharField(max_length=100)),
                ("mytitle", models.CharField(max_length=500)),
                ("mycontent", models.CharField(max_length=2000)),
                ("mydate", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="MyMember",
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
                ("myname", models.CharField(max_length=100)),
                ("mypassword", models.CharField(max_length=100)),
                ("myemail", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Reply",
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
                ("author", models.CharField(max_length=100)),
                ("content", models.CharField(max_length=2000)),
                ("reply_date", models.DateTimeField(auto_now_add=True)),
                (
                    "myboard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="myboard.myboard",
                    ),
                ),
            ],
        ),
    ]
