# Generated by Django 2.2.1 on 2019-05-24 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rc_dic', '0005_auto_20190524_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
