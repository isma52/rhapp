# Generated by Django 3.0.3 on 2020-04-15 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rhapp', '0005_remove_crh_op_perf'),
    ]

    operations = [
        migrations.AddField(
            model_name='crh',
            name='op_perf',
            field=models.CharField(default='N/A', max_length=200),
        ),
    ]
