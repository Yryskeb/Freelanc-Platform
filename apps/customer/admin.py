from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'company_name', 'balance', 'is_active')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name', 'company_name')
    list_filter = ('is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'company_name', 'balance')}),
        ('Permissions', {'fields': ('is_active', 'activation_code', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )

admin.site.register(Customer, CustomerAdmin)
