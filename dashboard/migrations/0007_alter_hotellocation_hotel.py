# Generated by Django 4.1.5 on 2023-08-10 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_hotellocation_hotel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotellocation',
            name='hotel',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='distance', to='dashboard.hotel', verbose_name='اسم الفندق'),
        ),
    ]
