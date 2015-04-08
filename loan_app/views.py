# -*- coding: utf-8 -*-
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from loan_app.models import Field, ApplicationType, Application
from loan_app.serializers import (
    FieldSerializer, ApplicationTypeSerializer, ApplicationSerializer
)


class FieldViewSet(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    @list_route(url_path='value-types')
    def value_types(self, request, *args, **kwargs):
        value_types = [
            value_type_model.get_key()
            for value_type_model
            in Field.VALUE_TYPE_MODELS
        ]
        return Response(value_types)


class ApplicationTypeViewSet(ModelViewSet):
    queryset = ApplicationType.objects.all()
    serializer_class = ApplicationTypeSerializer


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
