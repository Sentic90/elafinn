# Generated by Django 4.1.5 on 2023-08-08 09:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0065_remove_booking_room_booking_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='year',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='للعام'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='total_with_vat',
            field=models.FloatField(default=0, verbose_name='الاجمالي مع القيمة المضافة'),
        ),
    ]
