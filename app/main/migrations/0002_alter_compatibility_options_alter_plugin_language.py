# Generated by Django 4.1.5 on 2023-02-01 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="compatibility",
            options={"verbose_name_plural": "compatibilities"},
        ),
        migrations.AlterField(
            model_name="plugin",
            name="language",
            field=models.CharField(default="Unknown language", max_length=100),
        ),
    ]
