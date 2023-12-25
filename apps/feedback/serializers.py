from rest_framework import serializers
from apps.feedback.models import FreelancerRating, Favorite, FreelCommentOrder, FreelCommentCustomer, CustCommentFreel, CustCommentOrder
from apps.customer.models import Customer 
from apps.freelancer.models import Freelancer
from apps.order.models import Order


# Customer favorited and rated Freelancer

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'freelancer', 'customer']

class FreelancerRatingSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.id')
    freelancer = serializers.ReadOnlyField(source='freelancer.id')

    class Meta:
        model = FreelancerRating
        fields = '__all__'


# Freelancer comments to order and customer

class FreelCommentOrderSerializer(serializers.ModelSerializer):
    freelancer = serializers.PrimaryKeyRelatedField(queryset=Freelancer.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta: 
        model = FreelCommentOrder
        fields = ['id', 'freelancer', 'order', 'comment', 'created_at']

class FreelCommentCustomerSerializer(serializers.ModelSerializer):
    freelancer = serializers.PrimaryKeyRelatedField(queryset=Freelancer.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta: 
        model = FreelCommentCustomer
        fields = ['id', 'freelancer', 'customer', 'comment', 'created_at']


# Customer comments to freelancer and order

class CustCommentOrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta: 
        model = CustCommentOrder
        fields = ['id', 'customer', 'order', 'comment', 'created_at']

class CustCommentFreelSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    freelancer = serializers.PrimaryKeyRelatedField(queryset=Freelancer.objects.all())

    class Meta: 
        model = CustCommentFreel
        fields = ['id', 'customer', 'freelancer', 'comment', 'created_at']