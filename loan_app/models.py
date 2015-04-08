# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.loading import get_model


class ApplicationType(models.Model):
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=8)
    fields = models.ManyToManyField('loan_app.Field')

    def __unicode__(self):
        return u'{name}'.format(
            name=self.name,
        )


class Application(models.Model):
    application_type = models.ForeignKey('loan_app.ApplicationType')

    def __unicode__(self):
        return u'{type}-{number}'.format(
            type=self.application_type.short_name,
            number=self.pk,
        )


class Value(models.Model):
    field = models.ForeignKey('loan_app.Field')
    application = models.ForeignKey('loan_app.Application')

    _value = None
    _typified_value_object = None

    @property
    def value(self):
        typified_value_object = self.typified_value_object
        if typified_value_object:
            return typified_value_object.typified_value
        else:
            return self._value

    @value.setter
    def value(self, value):
        typified_value_object = self.typified_value_object
        if typified_value_object:
            typified_value_object.typified_value = value
        else:
            self._value = value

    def get_typified_value_model(self):
        field = self.field
        typified_value_model_name = field.value_type
        value_type_model = get_model(*typified_value_model_name.split('.'))
        return value_type_model

    @property
    def typified_value_object(self):
        if not self._typified_value_object:
            value_type_model = self.get_typified_value_model()
            try:
                self._typified_value_object = (
                    value_type_model.objects.get(pk=self.pk)
                )
            except value_type_model.DoesNotExist:
                pass
        return self._typified_value_object

    def save(self, *args, **kwargs):
        super(Value, self).save(*args, **kwargs)
        if hasattr(self, 'typified_value'):
            return
        typified_value_object = self.typified_value_object
        if not typified_value_object:
            value_type_model = self.get_typified_value_model()
            typified_value_object = value_type_model(
                value=self,
                typified_value=self._value
            )
            typified_value_object.__dict__.update(self.__dict__)
        typified_value_object.save()


class CharValue(Value):
    typified_value = models.CharField(max_length=512)


class TextValue(Value):
    typified_value = models.TextField()


class DateValue(Value):
    typified_value = models.DateField()


class DateTimeValue(Value):
    typified_value = models.DateTimeField()


class IntegerValue(Value):
    typified_value = models.IntegerField()


class BooleanValue(Value):
    typified_value = models.BooleanField()


class FloatValue(Value):
    typified_value = models.FloatField()


class Field(models.Model):
    VALUE_TYPE_MODELS = [
        CharValue,
        TextValue,
        DateValue,
        DateTimeValue,
        IntegerValue,
        BooleanValue,
        FloatValue,
    ]
    key = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    value_type = models.CharField(
        max_length=64,
        choices=(
            (
                u'{app_name}.{class_name}'.format(
                    app_name=value_type_model._meta.app_label,
                    class_name=value_type_model._meta.object_name,
                ),
                value_type_model.__name__
            )
            for value_type_model
            in VALUE_TYPE_MODELS
        )
    )

    def __unicode__(self):
        return u'{name}: {type}'.format(
            name=self.name,
            type=self.get_value_type_display(),
        )
