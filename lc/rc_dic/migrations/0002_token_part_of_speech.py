# Generated by Django 2.2.1 on 2019-05-13 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rc_dic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='part_of_speech',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
    ]
