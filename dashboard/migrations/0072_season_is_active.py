# Generated by Django 4.1.5 on 2023-08-08 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0071_alter_season_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
