# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from loan_app.views import FieldViewSet


router = DefaultRouter()
router.register(r'fields', FieldViewSet)

urlpatterns = [
    url(r'^rest/', include(router.urls)),
]
