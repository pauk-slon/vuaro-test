# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from loan_app.views import FieldViewSet, ApplicationTypeViewSet


router = DefaultRouter()
router.register(r'fields', FieldViewSet)
router.register(r'application-types', ApplicationTypeViewSet)

urlpatterns = [
    url(r'^rest/', include(router.urls)),
]
