from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from .managers import CustomUserManager
from django.utils import timezone
from multiselectfield import MultiSelectField

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=264, null=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_ip = models.GenericIPAddressField(null=False)
    country = models.CharField(max_length=128, null=False)
    state = models.CharField(max_length=64, null=False)
    timezone = models.CharField(max_length=128, null=False)
    os = models.CharField(max_length=24, null=False)

    def __str__(self):
        return self.name

class Company(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=150, unique=True, null=False)
    type_choices = [('Retailer', 'Retailer'), ('Provider', 'Provider')]
    type = models.CharField(choices=type_choices, max_length=12, null=False)
    dropshipping = models.BooleanField(default=False)
    city = models.CharField(max_length=24, null=False)
    postal_code = models.CharField(max_length=6, null=False)
    address = models.CharField(max_length=256, null=False)
    phone = models.CharField(max_length=24, null=False)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Store(models.Model):
    location = models.CharField(max_length=100, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='store_owner')

    def __str__(self):
        return self.location

class Product(models.Model):
    name = models.CharField(max_length=256, unique=True, null=False)
    brand = models.CharField(max_length=128, null=False)
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to = 'static/img/')

    def __str__(self):
        return self.name

class Stock(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    quantity = models.IntegerField(null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_stock')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_stock')
    product_features = models.CharField(max_length=256, null=True)

    def company_name(self):
        return self.store.company

    class Meta:
        unique_together = ('product', 'store', 'product_features')

MEMORY_CHOICES = (
    ('256GB+4GB', '256GB+4GB'),
    ('128GB+8GB', '128GB+8GB'),
    ('128GB+6GB', '128GB+6GB'),
    ('128GB+4GB', '128GB+4GB'),
    ('128GB+3GB', '128GB+3GB'),
    ('64GB+6GB', '64GB+6GB'),
    ('64GB+4GB', '64GB+4GB'),
    ('64GB+3GB', '64GB+3GB'),
    ('32GB+2GB', '32GB+2GB'),
    ('16GB+1GB', '16GB+1GB'),
)

class Smartphone(Product):
    #datos generales
    memory = MultiSelectField(choices=MEMORY_CHOICES, null=True)
    color = models.CharField(max_length=128, null=False)
    screen = models.CharField(max_length=32, null=False)
    battery = models.IntegerField()
    camera = models.DecimalField(max_digits=6, decimal_places=2)
    link = models.URLField(null=False)

# european_union = [
#     ('Austria', 'Austria'), ('Belgium', 'Belgium'), ('Bulgaria', 'Bulgaria'), ('Croatia', 'Croatia'), ('Cyprus', 'Cyprus'),
#     ('Czech Republic', 'Czech Republic'), ('Denmark', 'Denmark'), ('Estonia', 'Estonia'), ('Finland', 'Finland'), ('France', 'France'), ('Germany', 'Germany'),
#     ('Greece', 'Greece'), ('Hungary', 'Hungary'), ('Ireland', 'Ireland'), ('Italy', 'Italy'), ('Latvia', 'Latvia'), ('Lithuania', 'Lithuania'),
#     ('Luxembourg', 'Luxembourg'), ('Malta', 'Malta'), ('Netherlands', 'Netherlands'), ('Poland', 'Poland'), ('Portugal', 'Portugal'), ('Romania', 'Romania'),
#     ('Slovakia', 'Slovakia'), ('Slovenia', 'Slovenia'), ('Spain', 'Spain'), ('Sweden', 'Sweden'), ('United Kingdom', 'United Kingdom')
# ]
# shipping_restrictions = ArrayField(
#     models.CharField(max_length=32, choices=european_union, blank=True),
#     default=list,
#     blank=True
# )