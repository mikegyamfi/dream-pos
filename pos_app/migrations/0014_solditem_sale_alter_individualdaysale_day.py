# Generated by Django 4.2.4 on 2023-12-14 12:51

import datetime
from django.db import migrations, models
import django.db.models.deletion
import pos_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0013_alter_soldorder_closed_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualdaysale',
            name='day',
            field=models.DateField(default=datetime.date(2023, 12, 14)),
        ),
    ]
