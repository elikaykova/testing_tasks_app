# Generated by Django 2.1.3 on 2018-12-13 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20181213_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutioninstance',
            name='submition_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
