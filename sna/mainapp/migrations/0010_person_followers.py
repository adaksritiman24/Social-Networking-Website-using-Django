# Generated by Django 3.2.6 on 2021-10-05 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='followers',
            field=models.IntegerField(default=0),
        ),
    ]
