# Generated by Django 2.1.3 on 2018-12-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20181213_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_progress',
            field=models.FloatField(default=0),
        ),
    ]