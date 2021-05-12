from rest_framework import serializers, fields
from api.models import User, Profile, Company, Smartphone, Product, Store, Stock, MEMORY_CHOICES
from rest_framework.authtoken.models import Token
from django.conf import settings

class StockSerializer(serializers.ModelSerializer):

    company = serializers.ReadOnlyField(source='company.id')

    class Meta:
        model = Stock
        fields = ['id', 'company', 'store', 'product', 'price', 'quantity', 'product_features']

class StoreSerializer(serializers.ModelSerializer):

    company = serializers.ReadOnlyField(source='company.id')

    class Meta:
        model = Store
        fields = ['id', 'company', 'location']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'id']

class SmartphoneSerializer(serializers.ModelSerializer):

    image =  serializers.SerializerMethodField()
    memory = fields.MultipleChoiceField(choices=MEMORY_CHOICES)

    class Meta:
        model = Smartphone
        fields = ['id', 'name', 'brand', 'memory', 'date_added', 'image', 'color', 'screen', 'battery', 'camera', 'link']

    def get_image(self, obj):
        img = settings.API_URL + str(obj.image)
        img.replace(obj.name, '')
        return img.replace('/api/smartphones/', '')

class CompanySerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Company
        fields = ['id', 'owner', 'name', 'type', 'dropshipping', 'city', 'postal_code', 'address', 'phone', 'is_active', 'date_created']
        extra_kwargs = {
            'is_active': {'read_only': True},
            'date_created': {'read_only': True},
        }

class ProfileSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'name', 'date_joined', 'last_ip', 'country', 'state', 'timezone', 'os']
        extra_kwargs = {
            'date_joined': {'read_only': True},
        }

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id')
        read_only_fields = ('email', 'id')

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key', 'user')

class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
