# Generated by Django 3.1.3 on 2022-11-03 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order_date',
            field=models.DateField(),
        ),
    ]
