# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan_app', '0004_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(max_length=128, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
    ]
