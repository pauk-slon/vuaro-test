# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField

from loan_app.models import Field, ApplicationType


class FieldSerializer(ModelSerializer):
    class Meta:
        model = Field


class ApplicationTypeSerializer(ModelSerializer):
    fields = SlugRelatedField(
        many=True,
        slug_field='key',
        queryset=Field.objects.all(),
    )

    class Meta:
        model = ApplicationType
