from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Profile, Company, Smartphone, Store, Stock


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        #('Info', {'fields': ('company', 'profile')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class CustomSmartphone(admin.ModelAdmin):
    model = Smartphone
    list_display = ('name', 'brand', 'date_added',)
    list_filter = ('brand', 'date_added',)

class CustomStore(admin.ModelAdmin):
    model = Store
    list_display = ('company', 'location',)
    list_filter = ('company', 'location',)

class CustomStock(admin.ModelAdmin):
    model = Stock
    list_display = ('product', 'company_name', 'store', 'product_features', 'price', 'quantity')
    list_filter = ('store', 'product', 'price', 'quantity')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Smartphone, CustomSmartphone)
admin.site.register(Store, CustomStore)
admin.site.register(Stock, CustomStock)