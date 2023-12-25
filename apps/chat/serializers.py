from .models import Room, Customer, Freelancer, CustMessage, FreelMessage
from rest_framework import serializers
from apps.customer.serializers import CustUserSerializer
from apps.freelancer.serializers import FreelUserSerializer



class RoomSerializer(serializers.ModelSerializer):
    cust_host = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), default=None)
    freel_host = serializers.PrimaryKeyRelatedField(queryset=Freelancer.objects.all(), default=None)
    class Meta:
        model = Room
        fields = ['id', 'name', 'cust_host', 'freel_host', 'current_freel', 'current_cust']
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['current_freel'] = FreelUserSerializer(instance.current_freel.all(), many=True).data
        representation['current_cust'] = CustUserSerializer(instance.current_cust.all(), many=True).data
        return representation


class CustMessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = CustUserSerializer()

    class Meta:
        model = CustMessage
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj: CustMessage):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

class FreelMessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = FreelUserSerializer()

    class Meta:
        model = FreelMessage
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj: FreelMessage):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class CustRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = CustMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["pk", "name", "cust_host", "freel_host", "messages", "current_cust", "current_freel", "last_message"]
        depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj: Room):
        return CustMessageSerializer(obj.cust_messages.order_by('created_at').last()).data



class FreelRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = FreelMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["pk", "name", "cust_host", "freel_host", "messages", "current_cust", "current_freel", "last_message"]
        depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj: Room):
        return FreelMessageSerializer(obj.freel_messages.order_by('created_at').last()).data

