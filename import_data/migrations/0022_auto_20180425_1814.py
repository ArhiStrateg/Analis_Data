# Generated by Django 2.0.4 on 2018-04-25 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('import_data', '0021_auto_20180425_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume_hour_dont_win',
            name='sum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='resume_hour_win',
            name='sum',
            field=models.IntegerField(default=0),
        ),
    ]