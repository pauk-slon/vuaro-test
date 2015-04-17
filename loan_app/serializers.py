# -*- coding: utf-8 -*-
import itertools

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

    def to_internal_value(self, data):
        value_serializer = self.fields['values'].child
        field = value_serializer.fields['field']
        field.queryset = Field.objects.filter(
            application_type__key=data.get('application_type'),
        )
        return ModelSerializer.to_internal_value(self, data)

    def _get_available_field_keys(self, validated_data, only_non_empty=False):
        available_field_keys = [
            value_item['field'].key
            for value_item
            in validated_data['value_set']
            if not only_non_empty or 'typified_value' in value_item
        ]
        return available_field_keys

    def _check_required_fields_availability(self, validated_data):
        application_type = validated_data['application_type']
        fields = application_type.field_set
        required_fields = fields.filter(
            required=True
        )
        required_field_keys = [
            required_field.key
            for required_field
            in required_fields
        ]
        available_field_keys = self._get_available_field_keys(validated_data)
        for required_field_key in required_field_keys:
            if required_field_key not in available_field_keys:
                raise ValidationError(detail={
                    'values': "required field '{field_key}' is missed".format(
                        field_key=required_field_key
                    )
                })

    def _check_at_least_one_required_constraints(self, validated_data):
        application_type = validated_data['application_type']
        fields = application_type.field_set.all()
        at_least_one_required_fields = fields.exclude(
            at_least_one_required=u'',
        ).order_by(
            'at_least_one_required',
        )
        grouped_fields = itertools.groupby(
            at_least_one_required_fields,
            lambda f: f.at_least_one_required
        )
        non_empty_field_keys = self._get_available_field_keys(
            validated_data,
            only_non_empty=True
        )
        for at_least_one_required, group in grouped_fields:
            group_field_keys = [field.key for field in group]
            if all(
                field_key not in non_empty_field_keys
                for field_key in group_field_keys
            ):
                raise ValidationError(detail={
                    'values': (
                        'at least one form {field_keys} '
                        'has to be defined'.format(
                            field_keys=u', '.join(group_field_keys)
                        )
                    )
                })

    def create(self, validated_data):
        application_type = validated_data['application_type']
        self._check_required_fields_availability(validated_data)
        self._check_at_least_one_required_constraints(validated_data)
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
        if not self.partial:
            self._check_required_fields_availability(validated_data)
            self._check_at_least_one_required_constraints(validated_data)
            available_field_keys = self._get_available_field_keys(
                validated_data
            )
            application_type = instance.application_type
            not_required_field_keys = application_type.field_set.filter(
                required=False,
            ).values_list(
                'key',
                flat=True
            )
            missed_not_required_field_keys = (
                set(not_required_field_keys) - set(available_field_keys)
            )
            instance.value_set.filter(
                field__key__in=missed_not_required_field_keys
            ).delete()
        for value in validated_data['value_set']:
            field = value['field']
            if 'typified_value' not in value:
                instance.value_set.filter(
                    field=field
                ).delete()
                continue
            try:
                value_object = instance.value_set.get(field=field)
            except Value.DoesNotExist:
                value_object = Value(
                    field=field,
                    application=instance,
                )
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
