# Generated by Django 4.1 on 2023-07-04 12:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0003_solditem_payment_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Sales Personnel', 'Sales Personnel'), ('Admin', 'Admin'), ('Cashier', 'Cashier')], default='Sales Personnel', max_length=200),
        ),
        migrations.AlterField(
            model_name='individualdaysale',
            name='day',
            field=models.DateField(default=datetime.date(2023, 7, 4)),
        ),
    ]
