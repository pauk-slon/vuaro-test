# -*- coding: utf-8 -*-
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory

from loan_app.models import FieldType, ApplicationType, Field


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
    key = Sequence(lambda n: u'field-{0}'.format(n))
    name = Sequence(lambda n: u'поле {0}'.format(n))
    field_type = SubFactory(FieldTypeFactory)

    class Meta:
        model = Field
