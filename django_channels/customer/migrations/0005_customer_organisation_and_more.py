# Generated by Django 4.0.3 on 2022-05-26 08:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_remove_device_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='organisation',
            field=models.CharField(blank=0, default=django.utils.timezone.now, max_length=200, null=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='prefered_correspondence',
            field=models.CharField(blank=0, default=django.utils.timezone.now, max_length=5, null=0),
            preserve_default=False,
        ),
    ]
