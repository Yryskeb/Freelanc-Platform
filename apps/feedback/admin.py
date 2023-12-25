from django.contrib import admin
from apps.feedback.models import FreelancerRating, Favorite, FreelCommentCustomer, FreelCommentOrder, CustCommentFreel, CustCommentOrder

class FreelancerRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer', 'customer', 'rating', 'created_at')
    search_fields = ('freelancer__email', 'customer__email')
    list_filter = ('freelancer', 'customer', 'rating')

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer', 'customer')
    search_fields = ('freelancer__email', 'customer__email')

class FreelCommentOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer', 'comment', 'order', 'created_at')
    search_fields = ('freelancer__email', 'order__id')

class FreelCommentCustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer', 'customer', 'comment', 'created_at')
    search_fields = ('freelancer__email', 'customer__email')

class CustCommentOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'comment', 'created_at')
    search_fields = ('customer__email', 'order__id')

class CustCommentFreelAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'freelancer', 'comment', 'created_at')
    search_fields = ('customer__email', 'freelancer__email')

admin.site.register(FreelancerRating, FreelancerRatingAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(FreelCommentOrder, FreelCommentOrderAdmin)
admin.site.register(FreelCommentCustomer, FreelCommentCustomerAdmin)
admin.site.register(CustCommentOrder, CustCommentOrderAdmin)
admin.site.register(CustCommentFreel, CustCommentFreelAdmin)
