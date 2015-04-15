# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from loan_app.factories import (
    FieldFactory, ApplicationFactory, ApplicationTypeFactory
)
from loan_app.models import Application, Value
from loan_app.tests.rest_api.base import CreateUserTestCaseMixin


class PostApplicationApiTestCase(
    CreateUserTestCaseMixin,
    APITestCase,
):
    test_data_json_template = u"""{{
        "application_type": "{application_type}",
        "values": [
            {{
                "field": "{field}",
                "value": "{value}"
            }}
        ]
    }}"""

    def test_create(self):
        field = FieldFactory()
        value = u'тестовое значение'
        test_data = self.test_data_json_template.format(
            application_type=field.application_type.key,
            field=field.key,
            value=value,
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

    def test_not_required_fields(self):
        field = FieldFactory(required=False)
        test_data = self.test_data_json_template.format(
            application_type=field.application_type.key,
            field=field.key,
            value='',
        )
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.post(
            reverse('loan_app:application-list'),
            test_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        value_objects = Value.objects.all()
        self.assertEquals(value_objects.count(), 0)

    def test_required_fields(self):
        field = FieldFactory(required=True)
        test_data = self.test_data_json_template.format(
            application_type=field.application_type.key,
            field=field.key,
            value='',
        )
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.post(
            reverse('loan_app:application-list'),
            test_data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PutApplicationApiTestCase(
    CreateUserTestCaseMixin,
    APITestCase,
):
    def test_update_values(self):
        application = ApplicationFactory()
        test_data = {
            'id': application.id,
            'application_type': application.application_type.key,
            'values': [],
        }
        new_value = u'new value'
        for field_object in application.application_type.field_set.all():
            test_data[u'values'].append({
                'field': field_object.key,
                'value': new_value,
            })
        self.client.force_authenticate(user=self.get_django_superuser())
        path = reverse(
            viewname='loan_app:application-detail',
            kwargs={'pk': application.pk},
        )
        response = self.client.put(
            path,
            json.dumps(test_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        values = [
            value_object.value
            for value_object
            in application.value_set.all()
        ]
        self.assertEquals(
            application.application_type.field_set.count(),
            len(values),
        )
        self.assertTrue(
            all(value == new_value for value in values)
        )
        # if an unrequired value is empty,
        # the respective record has to be deleted
        not_required_fields = application.application_type.field_set.filter(
            required=False,
        )
        for field_object in not_required_fields:
            for value_item in test_data[u'values']:
                if value_item['field'] == field_object.key:
                    value_item['value'] = u''
        response = self.client.put(
            path,
            json.dumps(test_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        values = [
            value_object.value
            for value_object
            in application.value_set.all()
        ]
        required_fields = application.application_type.field_set.filter(
            required=True,
        )
        self.assertEquals(
            required_fields.count(),
            len(values),
        )
        not_required_values = application.value_set.filter(
            field__required=False
        )
        self.assertEquals(not_required_values.count(), 0)
        # if request doesn't contain an unrequired value,
        # the respective record has to be deleted
        for not_required_field in not_required_fields:
            new_value_object = Value(
                application=application,
                field=not_required_field,
            )
            new_value_object.value = new_value
            new_value_object.save()
        required_field_keys = [
            required_field.key
            for required_field
            in required_fields
        ]
        test_data[u'values'] = [
            value_item
            for value_item
            in test_data[u'values']
            if value_item['field'] in required_field_keys
        ]
        response = self.client.put(
            path,
            json.dumps(test_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(not_required_values.count(), 0)
        # if request doesn't contain any required value,
        # raise an exception
        self.assertTrue(
            required_fields.count(),
            msg=(
                u"the test application doesn't contain any required field,"
                u"this test cannot be executed correctly"
            )
        )
        test_data[u'values'] = []
        response = self.client.put(
            path,
            json.dumps(test_data),
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_regex_pattern_validation(self):
        application = ApplicationFactory()
        application_type = application.application_type
        values_data = []
        for field in application_type.field_set.all():
            field_type = field.field_type
            field_type.regex_pattern = u'^\d{5}$'
            field_type.save()
            values_data.append(
                {
                    'field': field.key,
                    'value': u'11111'
                }
            )
        test_data = {
            'application_type': application_type.key,
            'values': values_data,
        }
        path = reverse(
            viewname='loan_app:application-detail',
            kwargs={'pk': application.pk},
        )
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.put(
            path,
            json.dumps(test_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for value_item in test_data['values']:
            value_item['value'] = u'new_{old_value}'.format(
                old_value=value_item['value'],
            )
        response = self.client.put(
            path,
            json.dumps(test_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AtLeastOneRequiredValidationTestCase(
    CreateUserTestCaseMixin,
    APITestCase,
):
    def setUp(self):
        super(AtLeastOneRequiredValidationTestCase, self).setUp()
        self.application_type = ApplicationTypeFactory()
        at_least_one_required_group = 'at_leas_one_required'
        self.field_1 = FieldFactory(
            application_type=self.application_type,
            required=False,
            at_least_one_required=at_least_one_required_group,
        )
        self.field_2 = FieldFactory(
            application_type=self.application_type,
            required=False,
            at_least_one_required=at_least_one_required_group,
        )
        self.at_least_one_is_filled_test_data = {
            'application_type': self.application_type.key,
            'values': [
                {
                    'field': self.field_1.key,
                    'value': u'value-1'
                },
                {
                    'field': self.field_2.key,
                    'value': u''
                }
            ]
        }
        self.all_are_empty_test_data_list = [
            {
                'application_type': self.application_type.key,
                'values': [
                    {
                        'field': self.field_1.key,
                        'value': u''
                    },
                    {
                        'field': self.field_2.key,
                        'value': u''
                    },
                ],
            },
            {
                'application_type': self.application_type.key,
                'values': [
                    {
                        'field': self.field_1.key,
                        'value': u''
                    }
                ],
            },
            {
                'application_type': self.application_type.key,
                'values': [],
            },
        ]

    def test_create_at_least_one_is_filled(self):
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.post(
            reverse('loan_app:application-list'),
            json.dumps(self.at_least_one_is_filled_test_data),
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_create_all_are_empty(self):
        for test_data in self.all_are_empty_test_data_list:
            self.assert_bad_create_request(test_data)

    def assert_bad_create_request(self, data):
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.post(
            reverse('loan_app:application-list'),
            json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_at_least_one_is_filled(self):
        application = Application.objects.create(
            application_type=self.application_type,
            owner=self.get_django_superuser(),
        )
        path = reverse(
            viewname='loan_app:application-detail',
            kwargs={'pk': application.pk},
        )
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.put(
            path,
            json.dumps(self.at_least_one_is_filled_test_data),
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_update_all_are_empty(self):
        application = Application.objects.create(
            application_type=self.application_type,
            owner=self.get_django_superuser(),
        )
        path = reverse(
            viewname='loan_app:application-detail',
            kwargs={'pk': application.pk},
        )
        for test_data in self.all_are_empty_test_data_list:
            self.assert_bad_update_request(path, test_data)

    def assert_bad_update_request(self, path, data):
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.put(
            path,
            json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
