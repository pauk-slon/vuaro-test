# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField

from loan_app.models import (
    FieldType, Field, ApplicationType, Application, Value
)
from loan_app.value_serializers import ValueSerializer


class FieldTypeSerializer(ModelSerializer):
    class Meta:
        model = FieldType


class FieldSerializer(ModelSerializer):
    field_type = SlugRelatedField(
        slug_field='key',
        queryset=FieldType.objects.all(),
    )

    class Meta:
        model = Field
        exclude = (
            'application_type',
        )


class ApplicationTypeSerializer(ModelSerializer):
    fields = SlugRelatedField(
        many=True,
        slug_field='key',
        read_only=True,
        source='field_set',
    )

    class Meta:
        model = ApplicationType


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'groups',
        )


class ApplicationSerializer(ModelSerializer):
    application_type = SlugRelatedField(
        slug_field='key',
        queryset=ApplicationType.objects.all(),
    )
    values = ValueSerializer(many=True, source='value_set')
    owner = SlugRelatedField(slug_field='username', read_only=True)

    def create(self, validated_data):
        application = Application.objects.create(
            application_type=validated_data['application_type'],
            owner=validated_data['current_user'],
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
        return ModelSerializer.update(
            self,
            instance,
            validated_data_without_values
        )

    class Meta:
        model = Application
