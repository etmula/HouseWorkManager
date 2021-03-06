# Generated by Django 2.2.8 on 2020-12-02 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('work', '0003_auto_20201201_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Composite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='composites', to='accounts.Group')),
                ('parrent', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='composites', to='work.Composite')),
            ],
        ),
        migrations.RemoveField(
            model_name='work',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='work',
            name='parrent',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='works', to='work.Composite'),
        ),
    ]
