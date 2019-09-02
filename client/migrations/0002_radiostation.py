# Generated by Django 2.2.1 on 2019-06-11 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RadioStation',
            fields=[
                ('stationId', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('streamUrl', models.URLField(max_length=250)),
                ('desc', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('published', 'PUBLISHED'), ('unpublished', 'UNPUBLISHED')], default='unpublished', max_length=10)),
            ],
        ),
    ]