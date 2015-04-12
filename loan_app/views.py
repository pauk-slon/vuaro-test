# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from loan_app.models import FieldType, Field, ApplicationType, Application
from loan_app.permissions import (
    OwnerPolicyRestApiPermissions, OwnerPolicyPermissionHelper
)
from loan_app.serializers import (
    FieldTypeSerializer, FieldSerializer, ApplicationTypeSerializer,
    ApplicationSerializer, UserSerializer
)


class GetBySlugViewSetMixin(object):
    SLUG_FIELD_NAME = 'key'

    def get_object(self):
        try:
            return super(GetBySlugViewSetMixin, self).get_object()
        except Http404:
            queryset = self.filter_queryset(self.get_queryset())
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            filter_kwargs = {
                self.SLUG_FIELD_NAME: self.kwargs[lookup_url_kwarg]
            }
            return get_object_or_404(queryset, **filter_kwargs)


class UserViewSet(GetBySlugViewSetMixin, ModelViewSet):
    SLUG_FIELD_NAME = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FieldTypeViewSet(GetBySlugViewSetMixin, ModelViewSet):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer

    @list_route(url_path='value-types')
    def value_types(self, request, *args, **kwargs):
        value_types = [
            value_type_model.get_key()
            for value_type_model
            in Field.VALUE_TYPE_MODELS
        ]
        return Response(value_types)


class FieldViewSet(GetBySlugViewSetMixin, ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    @property
    def application_type_key(self):
        return self.kwargs['application_type_key']

    def get_application_type(self):
        try:
            return ApplicationType.objects.get(
                key=self.application_type_key
            )
        except ApplicationType.DoesNotExist:
            try:
                return ApplicationType.objects.get(
                    pk=self.application_type_key
                )
            except ApplicationType.DoesNotExist:
                pass
        raise Http404()

    def get_queryset(self):
        application_type = self.get_application_type()
        queryset = ModelViewSet.get_queryset(self)
        return queryset.filter(
            application_type__pk=application_type.pk
        )

    def perform_create(self, serializer):
        application_type = self.get_application_type()
        serializer.validated_data['application_type'] = application_type
        return ModelViewSet.perform_create(self, serializer)


class ApplicationTypeViewSet(GetBySlugViewSetMixin, ModelViewSet):
    queryset = ApplicationType.objects.all()
    serializer_class = ApplicationTypeSerializer


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [
        OwnerPolicyRestApiPermissions,
    ]

    def get_queryset(self):
        base_queryset = ModelViewSet.get_queryset(self)
        request = self.request
        user = request.user
        return OwnerPolicyPermissionHelper.filter_queryset(
            user=user,
            queryset=base_queryset,
        )

    def perform_create(self, serializer):
        serializer.validated_data['current_user'] = self.request.user
        return ModelViewSet.perform_create(self, serializer)
