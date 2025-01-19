from django.db import models
from django.contrib.auth.models import User
# control c for breaking 
class Item(models.Model):
    ITEM_CATEGORIES=[
        ('Shirt','Shirt'),
        ('Pants','Pants'),
        ('Jacket','Jacket'),
        ('Other','Other'),
    ]
    item_name=models.CharField(max_length=100)
    item_size=models.CharField(max_length=20)
    item_category=models.CharField(max_length=50,choices=ITEM_CATEGORIES,default='Other')
    item_count=models.PositiveIntegerField(default=0)
    item_price=models.PositiveIntegerField(default=0,null=True,blank=True)

class Transactions(models.Model):
    PAYMENT_MODES=[
        ('Online','Online'),
        ('Offline','Offline'),
        ('Both','Both'),
    ]
    item=models.ForeignKey(Item,on_delete=models.CASCADE,related_name="transactions")
    quantity_sold=models.PositiveIntegerField()
    selling_price_online=models.DecimalField(max_digits=10,decimal_places=2)
    selling_price_offline=models.DecimalField(max_digits=10,decimal_places=2)
    payment_mode=models.CharField(max_length=20,choices=PAYMENT_MODES,default='Offline')
    sold_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    sale_date=models.DateTimeField(auto_now_add=True)

class Profit(models.Model):
    total_expenses_on_clothes=models.PositiveIntegerField(default=0)
    total_expenses_on_shop=models.PositiveBigIntegerField(default=0)
    total_expenses_on_shopkeeper=models.PositiveIntegerField(default=0)
    total_expenses_on_other=models.PositiveIntegerField(default=0)
    gross_earning=models.PositiveIntegerField(default=0)
    gross_profit=models.PositiveIntegerField(default=0)
    cur_amount_on_counter=models.PositiveIntegerField(default=0)
    cur_amount_on_bank=models.PositiveIntegerField(default=0)
class Expenses(models.Model):
    user_name=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    expenses_on=models.CharField(max_length=100)
    expenses_mode=models.CharField(max_length=50)
    expenses_online=models.BigIntegerField(default=0)
    expenses_offline=models.BigIntegerField(default=0)
    expenses_date=models.DateTimeField(auto_now_add=True)
    