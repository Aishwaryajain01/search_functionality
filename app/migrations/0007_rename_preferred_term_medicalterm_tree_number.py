# Generated by Django 5.1 on 2024-09-17 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_selectedsuggestion_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicalterm',
            old_name='preferred_term',
            new_name='tree_number',
        ),
    ]
