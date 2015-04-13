# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from loan_app.factories import (
    ApplicationTypeFactory, FieldTypeFactory, FieldFactory
)
from loan_app.models import Field
from loan_app.tests.rest_api.base import (
    CreateUserTestCaseMixin, AssertAreFieldsEqualTestCaseMixin
)


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

    def test_update_field(self):
        field = FieldFactory(required=False)
        application_type = field.application_type
        url = reverse(
            viewname='loan_app:field-detail',
            kwargs={
                u'application_type_key': application_type.key,
                u'pk': field.key,
            },
        )
        field_type = field.field_type
        test_data = {
            'key': u'new-{field_key}'.format(field_key=field.key),
            'name': u'new-{field_name}'.format(field_name=field.name),
            'field_type': field_type.key,
            'required': True,
        }
        self.client.force_authenticate(user=self.get_django_superuser())
        response = self.client.put(url, test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = Field.objects.all()
        self.assertEquals(fields.count(), 1)
        self.assert_are_fields_equal(test_data, fields[0])
