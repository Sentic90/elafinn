# Generated by Django 4.1.5 on 2023-08-14 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_hotellocation_options_booking_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='ملاحظات'),
        ),
    ]
