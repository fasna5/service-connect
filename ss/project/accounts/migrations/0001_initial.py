# Generated by Django 5.1.1 on 2024-11-12 08:17

import accounts.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_type', models.CharField(choices=[('banner', 'Banner Ad'), ('card', 'Card Ad'), ('pop_up', 'Pop Up Ad')], max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('currency', models.CharField(default='INR', max_length=10)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=20)),
                ('total_views', models.IntegerField(blank=True, null=True)),
                ('total_hits', models.IntegerField(blank=True, null=True)),
                ('image_width', models.IntegerField()),
                ('image_height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category-images/', validators=[accounts.models.validate_file_size])),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Collar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('lead_quantity', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Country_Codes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=100, unique=True)),
                ('calling_code', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'ordering': ['calling_code'],
            },
        ),
        migrations.CreateModel(
            name='Franchise_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='INR', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeManagement',
            fields=[
                ('sl_no', models.AutoField(primary_key=True, serialize=False)),
                ('income_type', models.CharField(choices=[('Franchisee Registration', 'Franchisee Registration'), ('Service Registration', 'Service Registration'), ('Banner Ads', 'Banner Ads'), ('Card Ads', 'Card Ads'), ('Popup Ads', 'Popup Ads'), ('Boost Profile', 'Boost Profile'), ('Service Commission', 'Service Commission'), ('Lead Commission', 'Lead Commission')], max_length=50)),
                ('split_type', models.CharField(choices=[('Percentage', 'Percentage'), ('Amount', 'Amount')], default='Percentage', max_length=20)),
                ('company', models.IntegerField()),
                ('franchisee', models.IntegerField()),
                ('dealer', models.IntegerField()),
                ('service_provider', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Service_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('currency', models.CharField(blank=True, default='INR', max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100, null=True)),
                ('role', models.CharField(max_length=100)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='admin_pics/')),
                ('certifications', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Franchisee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_id', models.CharField(blank=True, editable=False, max_length=10, unique=True)),
                ('about', models.TextField()),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='f-profile_images/', validators=[accounts.models.validate_file_size])),
                ('revenue', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dealers', models.IntegerField(blank=True, null=True)),
                ('service_providers', models.IntegerField(blank=True, null=True)),
                ('valid_from', models.DateTimeField()),
                ('valid_up_to', models.DateTimeField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('verification_id', models.CharField(blank=True, max_length=255, null=True)),
                ('verificationid_number', models.CharField(blank=True, max_length=50, null=True)),
                ('community_name', models.CharField(max_length=50)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='franchisee_type', to='accounts.franchise_type')),
            ],
        ),
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_id', models.CharField(blank=True, editable=False, max_length=10, unique=True)),
                ('about', models.TextField()),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='d-profile-images/', validators=[accounts.models.validate_file_size])),
                ('service_providers', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('verification_id', models.CharField(blank=True, max_length=255, null=True)),
                ('verificationid_number', models.CharField(blank=True, max_length=50, null=True)),
                ('id_copy', models.FileField(blank=True, null=True, upload_to='id-dealer/', validators=[accounts.models.validate_file_size])),
                ('franchisee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.franchisee')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.PositiveIntegerField(editable=False, unique=True)),
                ('invoice_type', models.CharField(choices=[('service_request', 'Service Request'), ('dealer_payment', 'Dealer Payment'), ('provider_payment', 'Service Provider Payment'), ('service_registration', 'service_registration'), ('Ads', 'Ads'), ('lead_purchase', 'lead_purchase'), ('others', 'others')], max_length=20)),
                ('description', models.CharField(blank=True, max_length=30, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('partial_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('payment_balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('partially paid', 'partially paid'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('appointment_date', models.DateTimeField(blank=True, null=True)),
                ('additional_requirements', models.TextField(blank=True, null=True)),
                ('invoice_document', models.FileField(blank=True, null=True, upload_to='invoice-documents/', validators=[accounts.models.validate_file_size])),
                ('accepted_terms', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='received_payment', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sent_payment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=25)),
                ('order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('signature', models.CharField(blank=True, max_length=256, null=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('bank_transfer', 'Bank Transfer'), ('razorpay', 'razorpay'), ('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')], default='razorpay', max_length=50)),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='accounts.invoice')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='received_payments', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sent_payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_id', models.CharField(blank=True, editable=False, max_length=20, unique=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='s-profile-images/', validators=[accounts.models.validate_file_size])),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('about', models.TextField(blank=True, null=True)),
                ('address_proof_document', models.CharField(blank=True, max_length=255, null=True)),
                ('id_number', models.CharField(blank=True, max_length=50, null=True)),
                ('address_proof_file', models.FileField(blank=True, null=True, upload_to='id-service-pro/', validators=[accounts.models.validate_file_size])),
                ('payout_required', models.CharField(choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')], max_length=10)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('verification_by_dealer', models.CharField(choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('PENDING', 'Pending')], default='PENDING', max_length=20)),
                ('accepted_terms', models.BooleanField(default=False)),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.dealer')),
                ('franchisee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.franchisee')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number must be between 9 and 15 digits.', regex='^\\d{9,15}$')])),
                ('payment_method', models.CharField(choices=[('bank_transfer', 'Bank Transfer'), ('razorpay', 'razorpay'), ('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')], max_length=20)),
                ('account_holder_name', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=50)),
                ('bank_branch', models.CharField(max_length=50)),
                ('account_number', models.CharField(max_length=50)),
                ('ifsc_code', models.CharField(max_length=50)),
                ('supporting_documents', models.FileField(blank=True, null=True, upload_to='payment-request/', validators=[accounts.models.validate_file_size])),
                ('country_code', models.ForeignKey(blank=True, max_length=25, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.country_codes')),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_paymentrequest', to='accounts.dealer')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_paymentrequest', to='accounts.serviceprovider')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('description', models.TextField()),
                ('gstcode', models.CharField(max_length=50)),
                ('license', models.FileField(blank=True, null=True, upload_to='service-license/', validators=[accounts.models.validate_file_size])),
                ('image', models.ImageField(blank=True, null=True, upload_to='service-images/', validators=[accounts.models.validate_file_size])),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Inctive', max_length=10)),
                ('accepted_terms', models.BooleanField(default=False)),
                ('available_lead_balance', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='serviceregister_category', to='accounts.category')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='accounts.serviceprovider')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='service_register',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='serviceregister_invoices', to='accounts.serviceregister'),
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(editable=False, max_length=10, unique=True)),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('work_status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('acceptance_status', models.CharField(choices=[('accept', 'accept'), ('decline', 'decline'), ('pending', 'pending')], default='pending', max_length=20)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('availability_from', models.DateTimeField()),
                ('availability_to', models.DateTimeField()),
                ('additional_notes', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='service_request/', validators=[accounts.models.validate_file_size])),
                ('reschedule_status', models.BooleanField(default=False)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicerequest', to='accounts.serviceregister')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='service_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servicerequests_invoices', to='accounts.servicerequest'),
        ),
        migrations.CreateModel(
            name='DeclineServiceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decline_reason', models.TextField()),
                ('images', models.ImageField(blank=True, null=True, upload_to='decline/', validators=[accounts.models.validate_file_size])),
                ('service_requests', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='decline_services', to='accounts.servicerequest')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('images', models.ImageField(blank=True, null=True, upload_to='complaint/', validators=[accounts.models.validate_file_size])),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('resolution_notes', models.TextField(blank=True, null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='received_compliant', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sent_compliant', to=settings.AUTH_USER_MODEL)),
                ('service_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='complaints', to='accounts.servicerequest')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.state')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='subcategory-images/', validators=[accounts.models.validate_file_size])),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='accounts.category')),
                ('collar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='collar', to='accounts.collar')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='service_type', to='accounts.service_type')),
            ],
        ),
        migrations.AddField(
            model_name='serviceregister',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='serviceregister_subcategory', to='accounts.subcategory'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_customer', models.BooleanField(default=False)),
                ('is_service_provider', models.BooleanField(default=False)),
                ('is_franchisee', models.BooleanField(default=False)),
                ('is_dealer', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('full_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=30)),
                ('landmark', models.CharField(blank=True, max_length=255, null=True)),
                ('place', models.CharField(blank=True, max_length=20, null=True)),
                ('pin_code', models.CharField(max_length=10)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('watsapp', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be between 9 and 15 digits.', regex='^\\d{9,15}$')])),
                ('country_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.country_codes')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.district')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='app1_user_groups', to='auth.group', verbose_name='groups')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.state')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='app1_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_servicerequest', to='accounts.user'),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_servicerequest', to='accounts.user'),
        ),
        migrations.AddField(
            model_name='serviceprovider',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_provider', to='accounts.user'),
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp_received_user', to='accounts.user')),
            ],
        ),
        migrations.AddField(
            model_name='franchisee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='franchisee', to='accounts.user'),
        ),
        migrations.AddField(
            model_name='dealer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dealer', to='accounts.user'),
        ),
        migrations.CreateModel(
            name='CustomerReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])),
                ('image', models.ImageField(blank=True, null=True, upload_to='reviews/', validators=[accounts.models.validate_file_size])),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('service_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='servicerequest', to='accounts.servicerequest')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_review', to='accounts.user')),
                ('service_provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_review', to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_id', models.CharField(blank=True, editable=False, max_length=20, unique=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='c-profile-images/', validators=[accounts.models.validate_file_size])),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)),
                ('accepted_terms', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('landmark', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.CharField(max_length=20)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Ad_Management',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('valid_from', models.DateTimeField()),
                ('valid_up_to', models.DateTimeField()),
                ('target_area', models.CharField(choices=[('up_to_5_km', 'Up to 5 km'), ('up_to_10_km', 'Up to 10 km'), ('up_to_15_km', 'Up to 15 km')], default='up_to_5_km', max_length=100)),
                ('total_days', models.IntegerField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('image', models.ImageField(upload_to='ad_images/')),
                ('ad_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ad_category', to='accounts.ad_category')),
                ('ad_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ad_user', to='accounts.user')),
            ],
        ),
    ]
