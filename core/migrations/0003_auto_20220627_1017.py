# Generated by Django 2.2.13 on 2022-06-27 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220627_1013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='category_choice',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='label_choice',
            new_name='label',
        ),
    ]
