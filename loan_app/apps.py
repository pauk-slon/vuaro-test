# -*- coding: utf-8 -*-
from django.apps import AppConfig


class LoanAppConfig(AppConfig):
    name = 'loan_app'
    verbose_name = u'Заявки на кредит'

    def ready(self):
        AppConfig.ready(self)
