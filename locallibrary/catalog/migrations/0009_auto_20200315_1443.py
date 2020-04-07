# Generated by Django 2.2.10 on 2020-03-15 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20200315_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Выберите жанр книги', to='catalog.Genre'),
        ),
    ]
