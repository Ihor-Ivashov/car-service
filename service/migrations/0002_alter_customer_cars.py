# Generated by Django 4.1.7 on 2023-03-14 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cars',
            field=models.ManyToManyField(related_name='customers', to='service.car'),
        ),
    ]
