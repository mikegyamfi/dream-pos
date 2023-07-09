# Generated by Django 4.1 on 2023-07-09 08:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0007_cashiercart_created_at_alter_individualdaysale_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayssale',
            name='discount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='individualdaysale',
            name='day',
            field=models.DateField(default=datetime.date(2023, 7, 9)),
        ),
    ]
