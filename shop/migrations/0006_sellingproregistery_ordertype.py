# Generated by Django 3.1.3 on 2022-11-17 20:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20221118_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellingproregistery',
            name='orderType',
            field=models.CharField(choices=[('Single', 'Single'), ('Multiple', 'Multiple')], default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
    ]
