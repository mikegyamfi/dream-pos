# Generated by Django 4.1 on 2023-07-05 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pos_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0005_cart_cart_reference_cart_user_storeinfo_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashierCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_reference', models.CharField(blank=True, max_length=200, null=True)),
                ('domain', models.CharField(max_length=250)),
                ('product_qty', models.PositiveIntegerField()),
                ('unit_price', models.FloatField()),
                ('total_price', models.FloatField()),
                ('visited', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos_app.product')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=pos_app.models.get_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
