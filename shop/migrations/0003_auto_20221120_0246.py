# Generated by Django 3.1.3 on 2022-11-19 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_sellingproregistery_items'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='notifyyou',
            unique_together={('buyer', 'product_item')},
        ),
    ]