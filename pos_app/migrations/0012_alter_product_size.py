# Generated by Django 4.1 on 2023-06-24 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos_app', '0011_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos_app.size'),
        ),
    ]
