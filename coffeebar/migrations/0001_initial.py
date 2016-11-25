# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 22:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=8, verbose_name='Room number')),
                ('password', models.CharField(max_length=12, verbose_name='PIN Code')),
                ('owner_name', models.CharField(blank=True, max_length=150, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Opened'), (1, 'Closed'), (2, 'Suspended')])),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(choices=[(0, 'New'), (1, 'Processing'), (2, 'Done')], default=0)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coffeebar.Account')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default='1')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coffeebar.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('price', models.FloatField(default=0.0)),
                ('image', models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Addon',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='coffeebar.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='coffeebar.Product')),
                ('group', models.TextField(choices=[('Hot Coffee', 'Hot Coffee'), ('Cold Coffee', 'Cold Coffee'), ('Hot Tea', 'Hot Tea'), ('Cold Tea', 'Cold Tea')], editable=False, verbose_name='Drink group')),
                ('priority', models.IntegerField(default=0)),
                ('addons', models.ManyToManyField(to='coffeebar.Addon')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coffeebar.Product'),
        ),
    ]
