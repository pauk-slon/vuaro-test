# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('short_name', models.CharField(max_length=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=32)),
                ('name', models.CharField(max_length=64)),
                ('value_type', models.CharField(max_length=64, choices=[('loan_app.CharValue', b'CharValue'), ('loan_app.TextValue', b'TextValue'), ('loan_app.DateValue', b'DateValue'), ('loan_app.DateTimeValue', b'DateTimeValue'), ('loan_app.IntegerValue', b'IntegerValue'), ('loan_app.BooleanValue', b'BooleanValue'), ('loan_app.FloatValue', b'FloatValue')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
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
            model_name='applicationtype',
            name='fields',
            field=models.ManyToManyField(to='loan_app.Field'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='application_type',
            field=models.ForeignKey(to='loan_app.ApplicationType'),
            preserve_default=True,
        ),
    ]
