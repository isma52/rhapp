# Generated by Django 3.0.3 on 2020-04-29 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rhapp', '0017_auto_20200429_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='surname',
        ),
        migrations.AlterField(
            model_name='crh',
            name='comment',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='domain',
            name='manager',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='rhapp.Employee'),
        ),
        migrations.AlterField(
            model_name='project',
            name='domain',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='rhapp.Domain'),
        ),
        migrations.AlterField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='rhapp.Employee'),
        ),
    ]
