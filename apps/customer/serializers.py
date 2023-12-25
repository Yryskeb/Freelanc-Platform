from rest_framework import serializers 
from .models import Customer
from django.db.models import Avg
from apps.feedback.serializers import Favorite, FavoriteSerializer, CustCommentFreel, CustCommentFreelSerializer, FreelCommentCustomer, FreelCommentCustomerSerializer
from apps.order.serializers import OrderSerializer, Order


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    phone_number = serializers.CharField(required=True)
    
    class Meta:
        model = Customer 
        fields = ('balance', 'email', 'password', 'password_confirm', 'last_name', 'first_name', 'phone_number')
        ref_name = 'CustomerUserSerializer'

    def validate(self, attrs):
        phone_number = attrs['phone_number'].strip()
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise  serializers.ValidationError(
                'Passwords didnt match!'
            )
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                'Password feild must contain alpha and numeric symbols'
            )
        return attrs
    
    def create(self, validated_data):
        user = Customer.objects.create_user(**validated_data)
        return user
    
    


class CustUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer 
        exclude = ('password',)
        ref_name = 'CustomerUserSerializer'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        favorites = Favorite.objects.filter(customer=instance)
        favorite_data = FavoriteSerializer(instance=favorites, many=True).data
        repr['favorites'] = favorite_data

        orders = Order.objects.filter(customer=instance)
        order_data = OrderSerializer(instance=orders, many=True).data
        repr['history'] = order_data

        comments = FreelCommentCustomer.objects.filter(customer=instance)
        comments_data = FreelCommentCustomerSerializer(instance=comments, many=True).data
        repr['freel_comments'] = comments_data

        return repr
    