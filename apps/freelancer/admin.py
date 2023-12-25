from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Freelancer

class FreelancerAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'category', 'balance', 'is_active')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name', 'category__name', 'profession')
    list_filter = ('is_active', 'category')

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'birth_date', 'avatar', 'category', 'profession', 'what_i_can', 'price', 'work_time', 'city', 'balance')}),
        ('Permissions', {'fields': ('is_active', 'activation_code', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )

admin.site.register(Freelancer, FreelancerAdmin)
