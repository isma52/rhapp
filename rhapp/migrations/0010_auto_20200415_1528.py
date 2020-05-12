# Generated by Django 3.0.3 on 2020-04-15 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rhapp', '0009_auto_20200415_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crh',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rhapp.Employee', unique_for_month='date_crh'),
        ),
    ]
