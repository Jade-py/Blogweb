# Generated by Django 4.2.7 on 2024-03-24 02:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0024_alter_deadlines_ended_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deadlines',
            name='ended_on',
            field=models.DateField(default=datetime.date(2024, 3, 24)),
        ),
    ]
