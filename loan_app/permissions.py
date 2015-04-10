# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework.compat import get_model_name
from rest_framework.permissions import DjangoModelPermissions


class OwnerPolicyPermissionHelper(object):
    VIEW_ALL_PERM_PATTERN = '{app_label}.view_all_{model_name}'

    @classmethod
    def is_user_owner(cls, user, obj):
        return obj.owner == user

    @classmethod
    def filter_queryset(cls, user, queryset):
        model_cls = queryset.model
        view_all_perm_pattern = cls.VIEW_ALL_PERM_PATTERN
        view_all_perm = view_all_perm_pattern.format(
            app_label=model_cls._meta.app_label,
            model_name=get_model_name(model_cls),
        )
        if user.has_perm(view_all_perm):
            return queryset
        else:
            return queryset.filter(
                owner=user,
            )


class OwnerPolicyRestApiPermissions(DjangoModelPermissions):
    owner_policy_perms_map = {
        'GET': [OwnerPolicyPermissionHelper.VIEW_ALL_PERM_PATTERN],
        'PUT': ['{app_label}.change_all_{model_name}'],
        'PATCH': ['{app_label}.change_all_{model_name}'],
        'DELETE': ['{app_label}.delete_all_{model_name}'],
    }

    def has_object_permission(self, request, view, obj):
        owner_policy_perms_map = self.owner_policy_perms_map
        if obj and request.method in owner_policy_perms_map:
            kwargs = {
                'app_label': obj._meta.app_label,
                'model_name': obj._meta.model_name
            }
            perm_templates = owner_policy_perms_map[request.method]
            permissions = [
                perm_template.format(**kwargs)
                for perm_template
                in perm_templates

            ]
            user = request.user
            is_owner = OwnerPolicyPermissionHelper.is_user_owner(user, obj)
            has_owner_policy_perms = (
                user.has_perms(permissions) or is_owner
            )
            if not has_owner_policy_perms:
                return False
        return DjangoModelPermissions.has_permission(
            self, request, view
        )
