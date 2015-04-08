# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField, RelatedField

from loan_app.models import Field, ApplicationType, Application, Value
from loan_app.value_serializers import ValueSerializer


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


class ApplicationSerializer(ModelSerializer):
    application_type = SlugRelatedField(
        slug_field='key',
        queryset=ApplicationType.objects.all(),
    )
    values = ValueSerializer(many=True, source='value_set')

    def create(self, validated_data):
        application = Application.objects.create(
            application_type=validated_data['application_type']
        )
        for value in validated_data['value_set']:
            value_object = Value(
                application=application,
                field=value['field'],
                value=value['typified_value'],
            )
            value_object.save()
        return application

    def update(self, instance, validated_data):
        for value in validated_data['value_set']:
            field = value['field']
            value_object = instance.value_set.get(field=field)
            value_object.value = value['typified_value']
            value_object.save()
        validated_data_without_values = {
            item_key: item_value
            for (item_key, item_value)
            in validated_data.items()
            if item_key != 'value_set'
        }
        ModelSerializer.update(self, instance, validated_data_without_values)
        return instance

    class Meta:
        model = Application
