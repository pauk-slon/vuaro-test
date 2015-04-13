# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from loan_app.factories import FieldTypeFactory
from loan_app.models import FieldType
from loan_app.tests.rest_api.base import (
    CreateUserTestCaseMixin, AssertAreFieldsEqualTestCaseMixin
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
