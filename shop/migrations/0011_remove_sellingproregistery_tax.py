# Generated by Django 3.1.3 on 2022-11-18 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20221118_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellingproregistery',
            name='tax',
        ),
    ]
