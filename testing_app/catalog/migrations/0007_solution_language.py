# Generated by Django 2.1.3 on 2019-01-15 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_remove_solution_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='language',
            field=models.CharField(default='Python', max_length=64),
        ),
    ]
