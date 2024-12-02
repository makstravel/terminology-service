# Generated by Django 5.1.3 on 2024-12-02 22:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RefBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Уникальный код справочника.', max_length=100, unique=True, verbose_name='Код')),
                ('name', models.CharField(help_text='Наименование справочника.', max_length=300, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, help_text='Описание справочника.', verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50, verbose_name='Версия')),
                ('start_date', models.DateField(verbose_name='Дата начала действия версии')),
                ('refbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='terminology.refbook', verbose_name='Справочник')),
            ],
            options={
                'verbose_name': 'Версия справочника',
                'verbose_name_plural': 'Версии справочников',
                'ordering': ['-start_date', 'version'],
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, verbose_name='Код элемента')),
                ('value', models.CharField(max_length=300, verbose_name='Значение элемента')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='terminology.version', verbose_name='Версия')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочников',
                'ordering': ['code'],
            },
        ),
        migrations.AddConstraint(
            model_name='version',
            constraint=models.UniqueConstraint(fields=('refbook', 'start_date'), name='unique_start_date_per_refbook'),
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together={('refbook', 'version')},
        ),
        migrations.AddConstraint(
            model_name='element',
            constraint=models.UniqueConstraint(fields=('version', 'code'), name='unique_code_per_version'),
        ),
        migrations.AlterUniqueTogether(
            name='element',
            unique_together={('version', 'code')},
        ),
    ]