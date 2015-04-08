# -*- coding: utf-8 -*-
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField

from loan_app.models import (
    Field, Value, CharValue, TextValue, DateValue, DateTimeValue,
    IntegerValue, BooleanValue, FloatValue,
)


class TypifiedValueSerializerBase(ModelSerializer):
    field = SlugRelatedField(
        slug_field='key',
        queryset=Field.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        ModelSerializer.__init__(self, *args, **kwargs)
        self.fields['typified_value'].source = 'value'
        self.fields['typified_value'].field_name = 'value'

    def get_field_names(self, declared_fields, info):
        fields = ModelSerializer.get_field_names(self, declared_fields, info)
        if 'application' in fields:
            fields.remove('application')
        return fields


class CharValueSerializer(TypifiedValueSerializerBase):
    class Meta:
        model = CharValue


class TextValueSerializer(TypifiedValueSerializerBase):
    class Meta:
        model = TextValue


class DateValueSerializer(TypifiedValueSerializerBase):
    class Meta:
        model = DateValue


class DateTimeValueSerializer(TypifiedValueSerializerBase):
    class Meta:
        model = DateTimeValue


class IntegerValueSerializer(TypifiedValueSerializerBase):
    class Meta:
        model = IntegerValue


class BooleanValueSerializer(TypifiedValueSerializerBase):
    class Meta:
        model = BooleanValue


class FloatValueSerializer(TypifiedValueSerializerBase):
    class Meta:
        model = FloatValue


TYPIFIED_VALUE_SERIALIZERS_CLASS_LIST = [
    CharValueSerializer,
    TextValueSerializer,
    DateValueSerializer,
    DateTimeValueSerializer,
    IntegerValueSerializer,
    BooleanValueSerializer,
    FloatValueSerializer,
]

TYPIFIED_VALUE_SERIALIZERS_CLASS_DICT = {
    serializer_class.Meta.model: serializer_class
    for serializer_class
    in TYPIFIED_VALUE_SERIALIZERS_CLASS_LIST
}


class ValueSerializer(ModelSerializer):
    field = SlugRelatedField(
        slug_field='key',
        queryset=Field.objects.all(),
    )

    def to_internal_value(self, data):
        internal_value = ModelSerializer.to_internal_value(self, data)
        field = internal_value['field']
        typified_value_model = field.get_typified_value_model()
        typified_value_serializer_class = (
            TYPIFIED_VALUE_SERIALIZERS_CLASS_DICT.get(typified_value_model)
        )
        if not typified_value_serializer_class:
            raise APIException(
                'Serializer for {typified_value_model} is not defined'.format(
                    typified_value_model=typified_value_model
                )
            )
        typified_value_serializer = typified_value_serializer_class(data=data)
        typified_value_serializer.is_valid(raise_exception=True)
        return typified_value_serializer.validated_data

    class Meta:
        model = Value
        fields = ('field', 'value')
