# Generated by Django 4.0.3 on 2022-03-07 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0003_alter_product_nutrition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='limited_at',
        ),
        migrations.AddField(
            model_name='product',
            name='is_limited',
            field=models.BooleanField(default=False),
        ),
    ]
