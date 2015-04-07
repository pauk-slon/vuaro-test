# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models import get_models


for model in get_models():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
