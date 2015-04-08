# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer

from loan_app.models import Field


class FieldSerializer(ModelSerializer):
    class Meta:
        model = Field
