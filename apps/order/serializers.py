from rest_framework import serializers
from apps.order.models import Order, Proposal
from apps.freelancer.models import Freelancer 
from apps.customer.models import Customer
from apps.feedback.serializers import CustCommentOrder, CustCommentOrderSerializer, FreelCommentOrderSerializer, FreelCommentOrder


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), default=None)
    freelancer = serializers.PrimaryKeyRelatedField(queryset=Freelancer.objects.all(), default=None)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order 
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)

        customer_comments = CustCommentOrder.objects.filter(order=instance)
        customer_comments_data = CustCommentOrderSerializer(instance=customer_comments, many=True).data
        repr['customer_comments'] = customer_comments_data

        freelancer_comments = FreelCommentOrder.objects.filter(order=instance)
        freelancer_comments_data = FreelCommentOrderSerializer(instance=freelancer_comments, many=True).data
        repr['freelancer_comments'] = freelancer_comments_data

        return repr




class ProposalSerializer(serializers.ModelSerializer):
    freelancer = serializers.PrimaryKeyRelatedField(queryset=Freelancer.objects.all(), default=None)
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    
    class Meta:
        model = Proposal 
        fields = '__all__'