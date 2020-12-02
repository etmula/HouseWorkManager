# Generated by Django 2.2.8 on 2020-12-02 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0004_auto_20201202_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composite',
            name='parrent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='composites', to='work.Composite'),
        ),
        migrations.AlterField(
            model_name='work',
            name='parrent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='works', to='work.Composite'),
        ),
    ]
