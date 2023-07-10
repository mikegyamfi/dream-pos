# Generated by Django 4.1 on 2023-07-10 17:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0007_cashiercart_created_at_alter_individualdaysale_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dayssale',
            name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='dayssale',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='dayssale',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='dayssale',
            name='customer_phone',
        ),
        migrations.RemoveField(
            model_name='dayssale',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='dayssale',
            name='payment_mode',
        ),
        migrations.RemoveField(
            model_name='dayssale',
            name='user',
        ),
        migrations.AlterField(
            model_name='dayssale',
            name='total_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='individualdaysale',
            name='day',
            field=models.DateField(default=datetime.date(2023, 7, 10)),
        ),
        migrations.CreateModel(
            name='DaySaleOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=250)),
                ('sale_reference', models.CharField(max_length=200)),
                ('customer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('amount_paid', models.FloatField(blank=True, null=True)),
                ('balance', models.FloatField(blank=True, null=True)),
                ('payment_mode', models.CharField(choices=[('Cash', 'Cash'), ('Momo', 'Momo'), ('Card', 'Card')], default='Cash', max_length=100)),
                ('discount', models.CharField(blank=True, max_length=100, null=True)),
                ('total_price', models.FloatField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]