# Generated by Django 4.0.5 on 2022-06-15 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_site', '0011_alter_good_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='description',
            field=models.TextField(null=True),
        ),
    ]