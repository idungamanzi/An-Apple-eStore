# Generated by Django 5.1.4 on 2025-01-04 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('An_Apple', '0003_product_category_product_is_available_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='original_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('phone', 'Phone'), ('charger', 'Charger'), ('cable', 'Cable'), ('cover', 'Cover')], default='phone', max_length=50),
        ),
    ]
