# Generated by Django 2.1.3 on 2019-01-15 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20190115_1059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solution',
            options={'ordering': ['-submition_date', 'user']},
        ),
        migrations.AddField(
            model_name='solution',
            name='language',
            field=models.CharField(default='Python', max_length=64),
        ),
    ]
