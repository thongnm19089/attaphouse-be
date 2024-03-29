# Generated by Django 3.2.7 on 2021-10-25 09:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=225)),
                ('img', models.CharField(max_length=255)),
                ('detail', models.TextField()),
                ('price', models.FloatField(max_length=64)),
                ('rating', models.FloatField(max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='categories.category')),
            ],
            options={
                'db_table': 'item',
                'ordering': ['-created_at'],
            },
        ),
    ]
