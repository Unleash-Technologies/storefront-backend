# Generated by Django 4.0.6 on 2022-08-27 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_inventorydocument_creation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='barcode',
            field=models.CharField(default='', max_length=48),
        ),
        migrations.AddField(
            model_name='item',
            name='cost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='markup',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
