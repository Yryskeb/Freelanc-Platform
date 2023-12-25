
from django.contrib import admin
from .models import Order, Proposal

class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'freelancer', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description', 'client__user__username', 'freelancer__user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

class ProposalAdmin(admin.ModelAdmin):
    list_display = ('order', 'freelancer', 'bid_amount', 'created_at', 'is_accepted')
    list_filter = ('is_accepted',)
    search_fields = ('order__title', 'freelancer__user__username', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

admin.site.register(Order, OrderAdmin)
admin.site.register(Proposal, ProposalAdmin)
