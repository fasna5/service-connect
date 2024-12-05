# Generated by Django 5.1.1 on 2024-12-04 06:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_invoice_payment_paymentrequest_servicerequest_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad_category',
            name='ad_type',
            field=models.CharField(choices=[('banner', 'Banner Ad'), ('card', 'Card Ad'), ('pop_up', 'Pop Up Ad'), ('boosted_profile', 'Boosted Profile')], max_length=50),
        ),
        migrations.CreateModel(
            name='BlockedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_blocked', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('blocked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_user', to=settings.AUTH_USER_MODEL)),
                ('blocking_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocking_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]