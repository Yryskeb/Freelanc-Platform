from django.contrib import admin
from .models import Room, CustMessage, FreelMessage

class CustMessageInline(admin.StackedInline):
    model = CustMessage
    extra = 1

class FreelMessageInline(admin.StackedInline):
    model = FreelMessage
    extra = 1

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cust_host', 'freel_host')
    inlines = [CustMessageInline, FreelMessageInline]

class CustMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'created_at')

class FreelMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'user', 'created_at')

admin.site.register(Room, RoomAdmin)
admin.site.register(CustMessage, CustMessageAdmin)
admin.site.register(FreelMessage, FreelMessageAdmin)
