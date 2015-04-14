# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Permission
from factory import (
    Sequence, SubFactory, post_generation, LazyAttributeSequence
)
from factory.django import DjangoModelFactory

from loan_app.models import (
    FieldType, ApplicationType,
    Field, Application, Value
)


class FieldTypeFactory(DjangoModelFactory):
    key = Sequence(lambda n: u'string-type-{0}'.format(n))
    name = Sequence(lambda n: u'строка {0}-го типа'.format(n))
    value_type = 'loan_app.CharValue'

    class Meta:
        model = FieldType


class ApplicationTypeFactory(DjangoModelFactory):
    key = Sequence(lambda n: u'application-type-{0}'.format(n))
    name = Sequence(lambda n: u'тип анкеты №{0}'.format(n))
    short_name = Sequence(lambda n: u'Т{0}'.format(n))

    class Meta:
        model = ApplicationType


class FieldFactory(DjangoModelFactory):
    application_type = SubFactory(ApplicationTypeFactory)
    key = LazyAttributeSequence(
        lambda obj, num: u'{application_type}-{field_type}-{sequence}'.format(
            application_type=obj.application_type.key,
            field_type=obj.field_type.key,
            sequence=num,
        )
    )
    name = Sequence(lambda n: u'поле {0}'.format(n))
    field_type = SubFactory(FieldTypeFactory)

    class Meta:
        model = Field


class UserFactory(DjangoModelFactory):
    username = Sequence(lambda n: u'user-{0:02}'.format(n))

    @post_generation
    def add_permissions(self, create, extracted, **kwargs):
        change_application_permission = Permission.objects.get(
            codename='change_application'
        )
        self.user_permissions.add(change_application_permission)
        delete_application_permission = Permission.objects.get(
            codename='delete_application'
        )
        self.user_permissions.add(delete_application_permission)

    class Meta:
        model = User


class ApplicationFactory(DjangoModelFactory):
    application_type = SubFactory(ApplicationTypeFactory)
    owner = SubFactory(UserFactory)

    class Meta:
        model = Application

    @post_generation
    def fill_values(self, create, extracted, **kwargs):
        required_field = FieldFactory(
            key='required_field',
            application_type=self.application_type,
            required=True
        )
        FieldFactory(
            key='not_required_field',
            application_type=self.application_type,
            required=False,
        )
        value_object = Value(
            application=self,
            field=required_field,
            value=u'тестовое значение'
        )
        value_object.save()
