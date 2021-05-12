# Generated by Django 3.2 on 2021-04-21 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('type', models.CharField(choices=[('Retailer', 'Retailer'), ('Provider', 'Provider')], max_length=12)),
                ('dropshipping', models.BooleanField(default=False)),
                ('city', models.CharField(max_length=24)),
                ('postal_code', models.CharField(max_length=6)),
                ('address', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=24)),
                ('is_active', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('brand', models.CharField(max_length=128)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(upload_to='static/img/')),
            ],
        ),
        migrations.CreateModel(
            name='Smartphone',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.product')),
                ('memory', multiselectfield.db.fields.MultiSelectField(choices=[('256GB+4GB', '256GB+4GB'), ('128GB+8GB', '128GB+8GB'), ('128GB+6GB', '128GB+6GB'), ('128GB+4GB', '128GB+4GB'), ('128GB+3GB', '128GB+3GB'), ('64GB+6GB', '64GB+6GB'), ('64GB+4GB', '64GB+4GB'), ('64GB+3GB', '64GB+3GB'), ('32GB+2GB', '32GB+2GB'), ('16GB+1GB', '16GB+1GB')], max_length=94, null=True)),
                ('color', models.CharField(max_length=128)),
                ('screen', models.CharField(max_length=32)),
                ('battery', models.IntegerField()),
                ('camera', models.DecimalField(decimal_places=2, max_digits=6)),
                ('link', models.URLField()),
            ],
            bases=('api.product',),
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_owner', to='api.company')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=264)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_ip', models.GenericIPAddressField()),
                ('country', models.CharField(max_length=128)),
                ('state', models.CharField(max_length=64)),
                ('timezone', models.CharField(max_length=128)),
                ('os', models.CharField(max_length=24)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.IntegerField()),
                ('product_features', models.CharField(max_length=256, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_stock', to='api.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_stock', to='api.store')),
            ],
            options={
                'unique_together': {('product', 'store', 'product_features')},
            },
        ),
    ]
