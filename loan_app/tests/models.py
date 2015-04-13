# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase


from loan_app.factories import (
    ApplicationTypeFactory, FieldTypeFactory
)
from loan_app.models import (
    Field, Application, Value, CharValue
)


class ValueTestCase(TestCase):
    def test_value_creation(self):
        application_type = ApplicationTypeFactory()
        field_type = FieldTypeFactory()
        surname_field = Field.objects.create(
            application_type=application_type,
            field_type=field_type,
            key=u'surname',
            name=u'Фамилия',
        )
        user = User.objects.create()
        car_loan_application = Application.objects.create(
            application_type=application_type,
            owner=user,
        )
        test_surname_value = u'Петров'
        surname_value_object = Value(
            application=car_loan_application,
            field=surname_field,
            value=test_surname_value,
        )
        surname_value_object.save()
        char_values = CharValue.objects.filter(
            application=car_loan_application,
            field=surname_field,
        )
        self.assertEquals(char_values.count(), 1)
        self.assertEquals(char_values[0].value, test_surname_value)
        self.assertEquals(char_values[0].typified_value, test_surname_value)
        new_test_surname_value = u'Иванов'
        surname_value_object.value = new_test_surname_value
        surname_value_object.save()
        char_values = CharValue.objects.filter(
            application=car_loan_application,
            field=surname_field,
        )
        self.assertEquals(
            char_values[0].typified_value,
            new_test_surname_value,
        )
