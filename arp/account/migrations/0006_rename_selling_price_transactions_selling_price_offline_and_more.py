# Generated by Django 5.1.4 on 2025-01-18 16:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_profit_cur_amount_on_bank'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='selling_price',
            new_name='selling_price_offline',
        ),
        migrations.AddField(
            model_name='transactions',
            name='selling_price_online',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenses_on', models.CharField(max_length=100)),
                ('expenses_mode', models.CharField(max_length=50)),
                ('expenses_online', models.BigIntegerField(default=0)),
                ('expenses_offline', models.BigIntegerField(default=0)),
                ('expenses_date', models.DateTimeField(auto_now_add=True)),
                ('user_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
