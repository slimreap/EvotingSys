# Generated by Django 4.1.3 on 2022-12-08 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evoting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votes',
            name='vote_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
