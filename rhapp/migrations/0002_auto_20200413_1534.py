# Generated by Django 3.0.3 on 2020-04-13 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='dateBirth',
            new_name='date_birth',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='employeeNumber',
            new_name='employee_number',
        ),
    ]