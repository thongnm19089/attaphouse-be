# Generated by Django 3.2.7 on 2021-10-22 07:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('designs_and_builds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutDoor',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=225)),
                ('img', models.CharField(max_length=255)),
                ('price', models.FloatField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'outdoor',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RenovationDesign',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=225)),
                ('img', models.CharField(max_length=255)),
                ('price', models.FloatField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'renovationdesign',
                'ordering': ['-created_at'],
            },
        ),
    ]
