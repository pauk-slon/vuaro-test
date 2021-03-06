# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.loading import get_model
from django.contrib.auth.models import User


class ApplicationType(models.Model):
    key = models.SlugField(
        u'уникальный идентификатор',
        max_length=64,
        unique=True,
    )
    name = models.CharField(
        u'название',
        max_length=128,
    )
    short_name = models.CharField(
        u'краткое название',
        max_length=8,
    )

    def __unicode__(self):
        return u'{name}'.format(
            name=self.name,
        )

    class Meta:
        verbose_name = u'тип анкеты'
        verbose_name_plural = u'типы анкет'


class Application(models.Model):
    application_type = models.ForeignKey('loan_app.ApplicationType')
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return u'{type}#{number}'.format(
            type=self.application_type.short_name,
            number=self.pk,
        )

    class Meta:
        verbose_name = u'анкета'
        verbose_name_plural = u'анкеты'
        permissions = (
            ('view_all_application', 'Can see all applications'),
            ('change_all_application', 'Can change all applications'),
            ('delete_all_application', 'Can delete all applications'),
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

    @property
    def typified_value_object(self):
        if not self._typified_value_object:
            field = self.field
            field_type = field.field_type
            value_type_model = field_type.get_typified_value_model()
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
            field = self.field
            field_type = field.field_type
            value_type_model = field_type.get_typified_value_model()
            typified_value_object = value_type_model(
                value=self,
                typified_value=self._value
            )
            typified_value_object.__dict__.update(self.__dict__)
        typified_value_object.save()

    @classmethod
    def get_key(cls):
        return u'{app_name}.{class_name}'.format(
            app_name=cls._meta.app_label,
            class_name=cls._meta.object_name,
        )

    class Meta:
        verbose_name = u'значение поля'
        verbose_name_plural = u'значения полей'

    def __unicode__(self):
        value = getattr(self, 'typified_value', self.value)
        return u'{field_key}={field_value}'.format(
            field_key=self.field.key,
            field_value=value,
        )


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


class FieldType(models.Model):
    VALUE_TYPE_MODELS = [
        CharValue,
        TextValue,
        DateValue,
        DateTimeValue,
        IntegerValue,
        BooleanValue,
        FloatValue,
    ]
    key = models.SlugField(
        u'уникальный идентификатор',
        max_length=64,
        unique=True,
    )
    name = models.CharField(
        u'название',
        max_length=64,
        unique=True,
    )
    value_type = models.CharField(
        u'тип',
        max_length=64,
        choices=(
            (
                value_type_model.get_key(),
                value_type_model.__name__
            )
            for value_type_model
            in VALUE_TYPE_MODELS
        ),
        default=VALUE_TYPE_MODELS[0].get_key(),
    )
    regex_pattern = models.CharField(
        u'RegEx-шаблон',
        help_text=u'шаблон, которому должно соответствовать значение',
        max_length=256,
        blank=True,
        default=u'',
    )

    def get_typified_value_model(self):
        typified_value_model_name = self.value_type
        value_type_model = get_model(*typified_value_model_name.split('.'))
        return value_type_model

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'тип поля'
        verbose_name_plural = u'типы полей'


class Field(models.Model):
    application_type = models.ForeignKey(
        'loan_app.ApplicationType',
    )
    key = models.SlugField(
        u'уникальный идентификатор',
        max_length=64,
    )
    name = models.CharField(
        u'название',
        max_length=128,
    )
    field_type = models.ForeignKey(
        'loan_app.FieldType',
    )
    required = models.BooleanField(
        u'обязательное для заполнения',
        default=False
    )
    at_least_one_required = models.CharField(
        u'обязательно хотя бы одно',
        help_text=u'будет требоваться заполнение хотя бы одного поля '
                  u'из тех, у которых данное поле одинаково',
        max_length=128,
        blank=True,
        default=u'',
    )

    def __unicode__(self):
        return u'{name}: {type}'.format(
            name=self.name,
            type=self.field_type,
        )

    class Meta:
        verbose_name = u'поле'
        verbose_name_plural = u'поля'
        unique_together = (
            'application_type',
            'key',
        )
