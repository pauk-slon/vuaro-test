# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import Model


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
