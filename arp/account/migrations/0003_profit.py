# Generated by Django 5.1.4 on 2025-01-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_item_item_price_transactions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_expenses_on_clothes', models.PositiveIntegerField()),
                ('total_expenses_on_shop', models.PositiveBigIntegerField()),
                ('total_expenses_on_shopkeeper', models.PositiveIntegerField()),
                ('total_expenses_on_other', models.PositiveIntegerField()),
                ('gross_earning', models.PositiveIntegerField()),
                ('gross_profit', models.PositiveIntegerField()),
                ('cur_amount_on_counter', models.PositiveIntegerField()),
            ],
        ),
    ]
