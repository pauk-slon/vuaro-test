# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from loan_app.factories import ApplicationTypeFactory
from loan_app.models import ApplicationType
from loan_app.tests.rest_api.base import (
    CreateUserTestCaseMixin, AssertAreFieldsEqualTestCaseMixin
)


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
