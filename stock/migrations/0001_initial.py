# Generated by Django 4.1.3 on 2023-05-24 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0013_rename_itemgroup_itemcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockModificationDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(null=True)),
                ('modification_amount', models.FloatField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.item')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockTransferDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('receiving_warehouse_modified_items', models.ManyToManyField(related_name='stock_transfer_received', to='inventory.warehouse')),
                ('sender_warehouse_modified_items', models.ManyToManyField(related_name='stock_transfer_send', to='inventory.warehouse')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockRecountDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('modified_item_entry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stock.stockmodificationdocument')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
