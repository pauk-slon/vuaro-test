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
        ),
        migrations.CreateModel(
            name='ApplicationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('short_name', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=32)),
                ('name', models.CharField(max_length=64)),
                ('value_type', models.CharField(max_length=64, choices=[('loan_app.CharValue', b'CharValue'), ('loan_app.TextValue', b'TextValue'), ('loan_app.DateValue', b'DateValue'), ('loan_app.DateTimeValue', b'DateTimeValue'), ('loan_app.IntegerValue', b'IntegerValue'), ('loan_app.BooleanValue', b'BooleanValue'), ('loan_app.FloatValue', b'FloatValue')])),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='BooleanValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.BooleanField()),
            ],
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='CharValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.CharField(max_length=512)),
            ],
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='DateTimeValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.DateTimeField()),
            ],
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='DateValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.DateField()),
            ],
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='FloatValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.FloatField()),
            ],
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='IntegerValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.IntegerField()),
            ],
            bases=('loan_app.value',),
        ),
        migrations.CreateModel(
            name='TextValue',
            fields=[
                ('value_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loan_app.Value')),
                ('typified_value', models.TextField()),
            ],
            bases=('loan_app.value',),
        ),
        migrations.AddField(
            model_name='value',
            name='application',
            field=models.ForeignKey(to='loan_app.Application'),
        ),
        migrations.AddField(
            model_name='value',
            name='attribute',
            field=models.ForeignKey(to='loan_app.Attribute'),
        ),
        migrations.AddField(
            model_name='applicationtype',
            name='attributes',
            field=models.ManyToManyField(to='loan_app.Attribute'),
        ),
        migrations.AddField(
            model_name='application',
            name='application_type',
            field=models.ForeignKey(to='loan_app.ApplicationType'),
        ),
    ]
