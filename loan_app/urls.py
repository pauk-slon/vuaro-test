# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from loan_app.views import (
    FieldTypeViewSet, FieldViewSet, ApplicationTypeViewSet,
    ApplicationViewSet, UserViewSet
)


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'field-types', FieldTypeViewSet)
router.register(r'application-types', ApplicationTypeViewSet)
router.register(
    prefix=(
        r'application-types/(?P<application_type_key>[-a-zA-Z0-9_]+)/fields'
    ),
    viewset=FieldViewSet,
    base_name='field'
)
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    url(r'^rest/', include(router.urls)),
]
