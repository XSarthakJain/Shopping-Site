# Generated by Django 3.1.3 on 2022-11-18 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20221118_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellingproregistery',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='sellingproregistery',
            name='paidAmount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sellingproregistery',
            name='shippingCharge',
            field=models.IntegerField(default=0),
        ),
    ]
