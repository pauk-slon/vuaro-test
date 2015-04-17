# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APITestCase

from loan_app.factories import ApplicationFactory, UserFactory
from loan_app.models import Application
from loan_app.tests.rest_api.base import CreateUserTestCaseMixin


class ApplicationPermissionsApiTestCase(
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

    def _check_get_response(self, user, app_count, only_count=False):
        application_list_path = reverse('loan_app:application-list')
        self.client.force_authenticate(user=user)
        response = self.client.get(application_list_path)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), app_count)
        if not only_count:
            self.assertTrue(
                all(
                    data_item['owner'] == user.username
                    for data_item in response.data
                )
            )

    def test_view_list(self):
        user_1_app_count = 1
        user_2_app_count = 2
        user_1 = UserFactory()
        for _index in range(0, user_1_app_count):
            ApplicationFactory(owner=user_1)
        user_2 = UserFactory()
        for _index in range(0, user_2_app_count):
            ApplicationFactory(owner=user_2)
        app_count = user_1_app_count + user_2_app_count
        self.assertEquals(
            Application.objects.all().count(),
            app_count,
        )
        self._check_get_response(user_1, user_1_app_count)
        self._check_get_response(user_2, user_2_app_count)
        view_all_application_permission = Permission.objects.get(
            codename='view_all_application'
        )
        user_3 = UserFactory()
        user_3.user_permissions.add(view_all_application_permission)
        self._check_get_response(user_3, app_count, only_count=True)

    def test_change(self):
        user_1 = UserFactory()
        application = ApplicationFactory(owner=user_1)
        user_2 = UserFactory()
        view_all_application_permission = Permission.objects.get(
            codename='view_all_application'
        )
        user_2.user_permissions.add(
            view_all_application_permission
        )
        self.client.force_authenticate(user=user_2)
        application_path = reverse(
            viewname='loan_app:application-detail',
            kwargs={'pk': application.id},
        )
        response = self.client.put(
            path=application_path,
            data={},
        )
        self.client.force_authenticate(user=user_1)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(
            path=application_path,
            data={},
        )
        self.assertTrue(
            response.status_code not in (
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
            )
        )

    def test_change_all(self):
        user_1 = UserFactory()
        application = ApplicationFactory(owner=user_1)
        user_2 = UserFactory()
        view_all_application_permission = Permission.objects.get(
            codename='view_all_application'
        )
        user_2.user_permissions.add(view_all_application_permission)
        change_all_application_permission = Permission.objects.get(
            codename='change_all_application'
        )
        user_2.user_permissions.add(change_all_application_permission)
        self.client.force_authenticate(user=user_2)
        application_path = reverse(
            viewname='loan_app:application-detail',
            kwargs={'pk': application.id},
        )
        response = self.client.put(
            path=application_path,
            data={},
        )
        self.assertTrue(
            response.status_code not in (
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
            )
        )

    def test_delete(self):
        user_1 = UserFactory()
        application = ApplicationFactory(owner=user_1)
        user_2 = UserFactory()
        view_all_application_permission = Permission.objects.get(
            codename='view_all_application'
        )
        user_2.user_permissions.add(
            view_all_application_permission
        )
        application_path = reverse(
            viewname='loan_app:application-detail',
            kwargs={'pk': application.id},
        )
        self.client.force_authenticate(user=user_2)
        response = self.client.delete(
            path=application_path,
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.client.force_authenticate(user=user_1)
        response = self.client.delete(
            path=application_path,
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEquals(Application.objects.all().count(), 0)

    def test_delete_all(self):
        user_1 = UserFactory()
        application = ApplicationFactory(owner=user_1)
        user_2 = UserFactory()
        view_all_application_permission = Permission.objects.get(
            codename='view_all_application'
        )
        user_2.user_permissions.add(view_all_application_permission)
        delete_all_application_permission = Permission.objects.get(
            codename='delete_all_application'
        )
        user_2.user_permissions.add(
            delete_all_application_permission
        )
        application_path = reverse(
            viewname='loan_app:application-detail',
            kwargs={'pk': application.id},
        )
        self.client.force_authenticate(user=user_2)
        response = self.client.delete(
            path=application_path,
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEquals(Application.objects.all().count(), 0)
