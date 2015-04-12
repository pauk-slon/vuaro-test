# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from loan_app.factories import (
    ApplicationTypeFactory, FieldTypeFactory, FieldFactory
)
from loan_app.models import (
    ApplicationType, FieldType, Field, Application, Value, CharValue
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


class CreateUserTestCaseMixin(object):
    DJANGO_SUPERUSER_USERNAME = 'django_superuser_username'
    DJANGO_SUPERUSER_PASSWORD = 'django_superuser_password'

    def setUp(self):
        super(CreateUserTestCaseMixin, self).setUp()
        User.objects.create(
            username=self.DJANGO_SUPERUSER_USERNAME,
            password=self.DJANGO_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

    def get_django_superuser(self):
        return User.objects.get(username=self.DJANGO_SUPERUSER_USERNAME)


class AssertAreFieldsEqualTestCaseMixin(object):
    def assert_are_fields_equal(self, dict_object, model_object):
        for attribute_name, value in dict_object.items():
            object_field_value = getattr(model_object, attribute_name, None)
            if object_field_value is None:
                continue
            if isinstance(object_field_value, Model):
                object_value = getattr(
                    object_field_value,
                    'key',
                    object_field_value.pk,
                )
            else:
                object_value = object_field_value
            self.assertEquals(
                value,
                object_value
            )


class FieldTypeApiTestCase(
    CreateUserTestCaseMixin,
    AssertAreFieldsEqualTestCaseMixin,
    APITestCase
):
    def test_create_field_type(self):
        test_data = {
            'key': 'string',
            'name': u'строка',
            'value_type': 'loan_app.CharValue',
        }
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.post(
            reverse('loan_app:fieldtype-list'),
            test_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        field_types = FieldType.objects.all()
        self.assertEquals(field_types.count(), 1)
        self.assert_are_fields_equal(test_data, field_types[0])

    def test_get_by_key(self):
        field_type = FieldTypeFactory()
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.get(
            reverse(
                viewname='loan_app:fieldtype-detail',
                kwargs={
                    'pk': field_type.key
                },
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ApplicationTypeApiTestCase(
    CreateUserTestCaseMixin,
    AssertAreFieldsEqualTestCaseMixin,
    APITestCase
):
    def test_create_application_type(self):
        test_data = {
            'name': u'Автокредит',
            'short_name': u'АК',
            'key': u'car',
        }
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.post(
            reverse('loan_app:applicationtype-list'),
            test_data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        application_types = ApplicationType.objects.all()
        self.assertEquals(application_types.count(), 1)
        self.assert_are_fields_equal(test_data, application_types[0])

    def test_get_by_key(self):
        application_type = ApplicationTypeFactory()
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.get(
            reverse(
                viewname='loan_app:applicationtype-detail',
                kwargs={
                    'pk': application_type.key
                },
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FieldApiTestCase(
    CreateUserTestCaseMixin,
    AssertAreFieldsEqualTestCaseMixin,
    APITestCase
):
    def test_create_field(self):
        application_type = ApplicationTypeFactory()
        field_type = FieldTypeFactory()
        test_data = {
            'key': 'surname',
            'name': u'фамилия',
            'field_type': field_type.key,
            'required': True,
        }
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.post(
            reverse(
                viewname='loan_app:field-list',
                kwargs={
                    u'application_type_key': application_type.key,
                },
            ),
            test_data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        fields = Field.objects.all()
        self.assertEquals(fields.count(), 1)
        self.assert_are_fields_equal(test_data, fields[0])


class ApplicationApiTestCase(CreateUserTestCaseMixin,
    APITestCase,
):
    def test_create(self):
        field = FieldFactory()
        value = u'тестовое значение'
        test_data_json_template = u"""{{
            "application_type": "{application_type}",
            "values": [
                {{
                    "field": "{field_1}",
                    "value": "{value_1}"
                }}
            ]
        }}"""
        test_data = test_data_json_template.format(
            application_type=field.application_type.key,
            field_1=field.key,
            value_1=value,
        )
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.post(
            reverse('loan_app:application-list'),
            test_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        applications = Application.objects.all()
        self.assertEquals(applications.count(), 1)
        self.assertEquals(
            applications[0].application_type,
            field.application_type,
        )
        self.assertEquals(
            self.get_django_superuser(),
            applications[0].owner,
        )
        value_objects = applications[0].value_set.all()
        self.assertEquals(value_objects.count(), 1)
        self.assertEquals(value_objects[0].field, field)
        self.assertEquals(value_objects[0].value, value)
