# Generated by Django 4.1.7 on 2023-03-14 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_alter_customer_cars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='service.car'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderrow',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_rows', to='service.order'),
        ),
    ]