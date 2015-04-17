# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.management import create_permissions
from django.db import models, migrations


field_types = [
    {
        'key': 'string',
        'name': u'строка',
        'value_type': 'loan_app.CharValue',
    },
    {
        'key': 'text',
        'name': u'текст',
        'value_type': 'loan_app.TextValue',
    },
    {
        'key': 'date',
        'name': u'дата',
        'value_type': 'loan_app.DateValue',
    },
    {
        'key': 'datetime',
        'name': u'дата и время',
        'value_type': 'loan_app.DateTimeValue',
    },
    {
        'key': 'personal-inn',
        'name': u'ИНН (физ. лица)',
        'value_type': 'loan_app.CharValue',
        'regex_pattern': u'^\d{12}$',
    },
    {
        'key': 'organization-inn',
        'name': u'ИНН (юр. лица)',
        'value_type': 'loan_app.CharValue',
        'regex_pattern': u'^\d{10}$',
    },
    {
        'key': 'passport-rf',
        'name': u'пасспорт гражданина РФ',
        'value_type': 'loan_app.TextValue',
        'regex_pattern': u'^\d{2} \d{2} \d{6} \d{2}\.\d{2}\.\d{4} .{1,150}$',
    },
    {
        'key': 'integer',
        'name': u'целое число',
        'value_type': 'loan_app.IntegerValue',
    },
    {
        'key': 'float',
        'name': u'вещественное число',
        'value_type': 'loan_app.FloatValue',
    },
    {
        'key': 'boolean',
        'name': u'boolean',
        'value_type': 'loan_app.BooleanValue',
    },
    {
        'key': 'telephone-number',
        'name': u'номер телефона',
        'value_type': 'loan_app.CharValue',
        'regex_pattern': u'^\d{13}$',
    },
]


base_fields = [
    {
        'key': u'surname',
        'name': u'фамилия',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'given_name',
        'name': u'имя',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'patronymic',
        'name': u'отчество',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'international-surname',
        'name': u'фамилия из загранпаспорта',
        'field_type': 'string',
        'required': False,
    },
    {
        'key': u'birthday',
        'name': u'дата рождения',
        'field_type': 'date',
        'required': True,
    },
    {
        'key': u'birthplace',
        'name': u'место рождения',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'citizenship',
        'name': u'гражданство',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'former-name',
        'name': u'прошлое фамилия и имя',
        'field_type': 'string',
        'required': False,
    },
    {
        'key': u'gender',
        'name': u'пол',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'passport-rf',
        'name': u'паспорт',
        'field_type': 'passport-rf',
        'required': True,
    },
    {
        'key': u'inn',
        'name': u'ИНН',
        'field_type': 'personal-inn',
        'required': False,
    },
    {
        'key': u'driver-license',
        'name': u'водительское удостоверение',
        'field_type': 'string',
        'required': False,
    },
    {
        'key': u'international-passport',
        'name': u'загранпаспорт',
        'field_type': 'string',
        'required': False,
    },
    {
        'key': u'army-id-card',
        'name': u'военный билет',
        'field_type': 'string',
        'required': False,
    },
    {
        'key': u'snils',
        'name': u'СНИЛС',
        'field_type': 'string',
        'required': False,
    },
    {
        'key': u'telephone-number-mobile',
        'name': u'телефон мобильный',
        'field_type': 'telephone-number',
        'required': False,
        'at_least_one_required': 'telephone-number',
    },
    {
        'key': u'telephone-number-home',
        'name': u'телефон домашний',
        'field_type': 'telephone-number',
        'required': False,
        'at_least_one_required': 'telephone-number',
    },
    {
        'key': u'telephone-number-work',
        'name': u'телефон рабочий',
        'field_type': 'telephone-number',
        'required': False,
        'at_least_one_required': 'telephone-number',
    },
    {
        'key': u'registration-address',
        'name': u'адрес регистрации',
        'field_type': 'text',
        'required': True,
    },
    {
        'key': u'habitation-address',
        'name': u'адрес проживания',
        'field_type': 'text',
        'required': True,
    },
    {
        'key': u'education',
        'name': u'образование',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'student',
        'name': u'студент',
        'field_type': 'boolean',
        'required': True,
    },
    {
        'key': u'marital-status',
        'name': u'семейное положение',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'job',
        'name': u'место работы',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'employer-inn',
        'name': u'ИНН организации',
        'field_type': 'organization-inn',
        'required': True,
    },
    {
        'key': u'employer-ogrn',
        'name': u'ОГРН огранизации',
        'field_type': 'string',
        'required': True,
    },
    {
        'key': u'employer-registration-address',
        'name': u'юр адрес организации ',
        'field_type': 'text',
        'required': True,
    },
    {
        'key': u'employer-habituation-address',
        'name': u'фактический адрес организации ',
        'field_type': 'text',
        'required': True,
    },
    {
        'key': u'employer-telephone-number',
        'name': u'телефон организации',
        'field_type': 'telephone-number',
        'required': True,
    },
]


application_types = [
    {
        'key': 'car-loan',
        'name': u'Автокредит',
        'short_name': u'АК',
        'fields': base_fields + [
            {
                'key': u'car-type',
                'name': u'тип авто (новая отечественная, '
                        u'новая иномарка, подержанная иномарка)',
                'field_type': 'string',
                'required': True,
            },
            {
                'key': u'down-payment',
                'name': u'первоначальный взнос (руб)',
                'field_type': 'float',
                'required': True,
            },
        ]
    },
    {
        'key': 'pos-loan',
        'name': u'Потреб кредит',
        'short_name': u'ПК',
        'fields': base_fields,
    },
    {
        'key': 'mortgage',
        'name': u'Ипотека',
        'short_name': u'ИК',
        'fields': base_fields + [
            {
                'key': u'property-type',
                'name': u'тип недвижомсти (новостройка, вторичка, '
                        u'участок, дом)',
                'field_type': 'telephone-number',
                'required': True,
            },
            {
                'key': u'down-payment',
                'name': u'первоначальный взнос (руб)',
                'field_type': 'float',
                'required': True,
            },
        ]
    }
]


groups = {
    'loan_app_user': [
        'change_application',
        'delete_application',
    ],
    'loan_app_bank_clerk': [
        'change_application',
        'delete_application',
        'view_all_application',
    ],
    'loan_app_superuser': [
        'change_application',
        'delete_application',
        'view_all_application',
        'change_all_application',
        'delete_all_application',
    ]
}


def add_field_types(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FieldType = apps.get_model('loan_app', 'FieldType')
    for field_type_dict in field_types:
        FieldType.objects.create(**field_type_dict)


def reverse_add_field_types(apps, schema_editor):
    keys = [field_type_dict['key'] for field_type_dict in field_types]
    FieldType = apps.get_model('loan_app', 'FieldType')
    FieldType.objects.filter(
        key__in=keys,
    ).delete()


def add_application_types(apps, schema_editor):
    ApplicationType = apps.get_model('loan_app', 'ApplicationType')
    FieldType = apps.get_model('loan_app', 'FieldType')
    field_type_object_dict = {
        field_type_object.key: field_type_object
        for field_type_object
        in FieldType.objects.all()
    }
    Field = apps.get_model('loan_app', 'Field')
    for application_type_dict in application_types:
        application_type_initial_dict = {
            key: value for key, value
            in application_type_dict.items()
            if not isinstance(value, list)
        }
        application_type = ApplicationType.objects.create(
            **application_type_initial_dict
        )
        for field_dict in application_type_dict['fields']:
            field_initial_dict = {
                key: value for key, value in field_dict.items()
                if key != 'field_type'
            }
            field_type_key = field_dict['field_type']
            field_type_objects = field_type_object_dict[field_type_key]
            field_initial_dict['field_type'] = field_type_objects
            field_initial_dict['application_type'] = application_type
            field_object = Field(**field_initial_dict)
            field_object.save()


def reverse_add_application_types(apps, schema_editor):
    application_type_keys = [
        application_type_dict['key']
        for application_type_dict
        in application_types
    ]
    ApplicationType = apps.get_model('loan_app', 'ApplicationType')
    ApplicationType.objects.filter(
        key__in=application_type_keys
    ).delete()


def add_groups(apps, schema_editor):
    app_config = apps.app_configs['loan_app']
    app_config.models_module = True
    create_permissions(app_config, verbosity=1)
    permission_codename_list = set(
        reduce(
            lambda acc, el: acc + el,
            groups.values()
        )
    )
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    permissions_dict = {
        permission_codename: Permission.objects.get(
            codename=permission_codename
        ) for permission_codename
        in permission_codename_list
    }
    for group_name, permission_codenames in groups.items():
        group_object = Group.objects.create(name=group_name)
        for permission_codename in permission_codenames:
            permission = permissions_dict[permission_codename]
            group_object.permissions.add(permission)


def reverse_add_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(
        name__in=groups.keys()
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('loan_app', '0003_field_at_least_one_required'),
    ]

    operations = [
        migrations.RunPython(
            code=add_field_types,
            reverse_code=reverse_add_field_types,
        ),
        migrations.RunPython(
            code=add_application_types,
            reverse_code=reverse_add_application_types,
        ),
        migrations.RunPython(
            code=add_groups,
            reverse_code=reverse_add_application_types,
        ),
    ]
