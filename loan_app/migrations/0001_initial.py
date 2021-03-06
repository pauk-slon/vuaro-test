# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u0430\u043d\u043a\u0435\u0442\u0430',
                'verbose_name_plural': '\u0430\u043d\u043a\u0435\u0442\u044b',
                'permissions': (('view_all_application', 'Can see all applications'), ('change_all_application', 'Can change all applications'), ('delete_all_application', 'Can delete all applications')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.SlugField(unique=True, max_length=64, verbose_name='\u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440')),
                ('name', models.CharField(max_length=128, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('short_name', models.CharField(max_length=8, verbose_name='\u043a\u0440\u0430\u0442\u043a\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0442\u0438\u043f \u0430\u043d\u043a\u0435\u0442\u044b',
                'verbose_name_plural': '\u0442\u0438\u043f\u044b \u0430\u043d\u043a\u0435\u0442',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.SlugField(max_length=64, verbose_name='\u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440')),
                ('name', models.CharField(max_length=128, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('required', models.BooleanField(default=False, verbose_name='\u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u0434\u043b\u044f \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f')),
                ('application_type', models.ForeignKey(to='loan_app.ApplicationType')),
            ],
            options={
                'verbose_name': '\u043f\u043e\u043b\u0435',
                'verbose_name_plural': '\u043f\u043e\u043b\u044f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.SlugField(unique=True, max_length=64, verbose_name='\u0443\u043d\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440')),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('value_type', models.CharField(default='loan_app.CharValue', max_length=64, verbose_name='\u0442\u0438\u043f', choices=[('loan_app.CharValue', b'CharValue'), ('loan_app.TextValue', b'TextValue'), ('loan_app.DateValue', b'DateValue'), ('loan_app.DateTimeValue', b'DateTimeValue'), ('loan_app.IntegerValue', b'IntegerValue'), ('loan_app.BooleanValue', b'BooleanValue'), ('loan_app.FloatValue', b'FloatValue')])),
            ],
            options={
                'verbose_name': '\u0442\u0438\u043f \u043f\u043e\u043b\u044f',
                'verbose_name_plural': '\u0442\u0438\u043f\u044b \u043f\u043e\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043f\u043e\u043b\u044f',
                'verbose_name_plural': '\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u043f\u043e\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.TextField()),
            ],
            options={
            },
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='IntegerValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.IntegerField()),
            ],
            options={
            },
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='FloatValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.FloatField()),
            ],
            options={
            },
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='DateValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.DateField()),
            ],
            options={
            },
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='DateTimeValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.DateTimeField()),
            ],
            options={
            },
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='CharValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.CharField(max_length=512)),
            ],
            options={
            },
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='BooleanValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.BooleanField()),
            ],
            options={
            },
            bases=('loan_app.value',),
        ),
        migrations.AddField(
            model_name='value',
            name='application',
            field=models.ForeignKey(to='loan_app.Application'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='value',
            name='field',
            field=models.ForeignKey(to='loan_app.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='field',
            name='field_type',
            field=models.ForeignKey(to='loan_app.FieldType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='field',
            unique_together=set([('application_type', 'key')]),
        ),
        migrations.AddField(
            model_name='application',
            name='application_type',
            field=models.ForeignKey(to='loan_app.ApplicationType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
