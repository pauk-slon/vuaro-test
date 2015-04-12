# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

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
    fields = FieldSerializer(
        many=True,
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
        application_type = validated_data['application_type']
        required_fields = application_type.field_set.filter(
            required=True
        )
        required_field_keys = [
            required_field.key
            for required_field
            in required_fields
        ]
        available_value_keys = [
            value_item['field'].key
            for value_item
            in validated_data['value_set']
        ]
        for required_field_key in required_field_keys:
            if required_field_key not in available_value_keys:
                raise ValidationError(detail={
                    'values': "required field '{field_key}' is missed".format(
                        field_key=required_field_key
                    )
                })
        application = Application.objects.create(
            application_type=application_type,
            owner=validated_data['current_user'],
        )

        for value in validated_data['value_set']:
            if 'typified_value' not in value:
                continue
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
