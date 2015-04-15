# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan_app', '0002_fieldtype_regex_pattern'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='at_least_one_required',
            field=models.CharField(default='', help_text='\u0431\u0443\u0434\u0435\u0442 \u0442\u0440\u0435\u0431\u043e\u0432\u0430\u0442\u044c\u0441\u044f \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u0445\u043e\u0442\u044f \u0431\u044b \u043e\u0434\u043d\u043e\u0433\u043e \u043f\u043e\u043b\u044f \u0438\u0437 \u0442\u0435\u0445, \u0443 \u043a\u043e\u0442\u043e\u0440\u044b\u0445 \u0434\u0430\u043d\u043d\u043e\u0435 \u043f\u043e\u043b\u0435 \u043e\u0434\u0438\u043d\u0430\u043a\u043e\u0432\u043e', max_length=128, verbose_name='\u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e \u0445\u043e\u0442\u044f \u0431\u044b \u043e\u0434\u043d\u043e', blank=True),
            preserve_default=True,
        ),
    ]
