# Generated by Django 2.0.1 on 2018-01-31 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20180131_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='telegram_id',
            field=models.IntegerField(blank=True, default=None, null=True, unique=True, verbose_name='ID telegram'),
        ),
    ]
