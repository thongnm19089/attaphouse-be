# Generated by Django 3.2.7 on 2021-10-19 10:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('uploads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RenovationForm',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255)),
                ('type_property', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('property_location', models.CharField(blank=True, max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('floor_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='floor_plan_renovation_form', to='uploads.file')),
                ('house_design', models.ManyToManyField(blank=True, related_name='house_design_renovation_form', to='uploads.File')),
            ],
            options={
                'db_table': 'renovation_form',
                'ordering': ['-created_at'],
            },
        ),
    ]
