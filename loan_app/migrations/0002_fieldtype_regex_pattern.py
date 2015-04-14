# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtype',
            name='regex_pattern',
            field=models.CharField(default='', help_text='\u0448\u0430\u0431\u043b\u043e\u043d, \u043a\u043e\u0442\u043e\u0440\u043e\u043c\u0443 \u0434\u043e\u043b\u0436\u043d\u043e \u0441\u043e\u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u043e\u0432\u0430\u0442\u044c \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', max_length=256, verbose_name='RegEx-\u0448\u0430\u0431\u043b\u043e\u043d', blank=True),
            preserve_default=True,
        ),
    ]
