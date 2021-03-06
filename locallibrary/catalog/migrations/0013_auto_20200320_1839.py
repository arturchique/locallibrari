# Generated by Django 2.2.10 on 2020-03-20 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_auto_20200315_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.BigIntegerField(help_text='Поставьте оценку')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Rating'),
        ),
    ]
