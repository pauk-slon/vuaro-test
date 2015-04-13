# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from loan_app.factories import FieldFactory, ApplicationFactory
from loan_app.models import Application, Value
from loan_app.tests.rest_api.base import CreateUserTestCaseMixin


class ApplicationApiTestCase(
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
