# -*- coding: utf-8 -*-
from django.test import TestCase

from loan_app.models import Field, ApplicationType, Application, Value, CharValue


class ValueTestCase(TestCase):
    def test_value_creation(self):
        surname_field = Field.objects.create(
            key=u'surname',
            name=u'Фамилия',
            value_type=u'loan_app.CharValue',
        )
        car_loan_application_type = ApplicationType.objects.create(
            name=u'Автокредит',
            short_name=u'АК',
        )
        car_loan_application_type.fields.add(surname_field)
        car_loan_application = Application.objects.create(
            application_type=car_loan_application_type
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
