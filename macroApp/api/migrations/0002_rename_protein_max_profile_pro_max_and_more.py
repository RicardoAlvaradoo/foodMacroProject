# Generated by Django 5.0.4 on 2024-07-03 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='protein_max',
            new_name='pro_max',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='protein_min',
            new_name='pro_min',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='name',
            new_name='profile_name',
        ),
    ]
