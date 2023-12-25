from django.db import models
from apps.customer.models import Customer
from apps.freelancer.models import Freelancer

class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    cust_host = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cust_rooms", blank=True, null=True)
    freel_host = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name="freel_rooms", blank=True, null=True)
    current_freel = models.ManyToManyField(Freelancer, related_name="freel_current_rooms", blank=True)
    current_cust = models.ManyToManyField(Customer, related_name="cust_current_rooms", blank=True)

    def __str__(self):
        return f"Room({self.id}. {self.name})"


class CustMessage(models.Model):
    room = models.ForeignKey("chat.Room", on_delete=models.CASCADE, related_name="cust_messages")
    text = models.TextField(max_length=500)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cust_messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.user} {self.room})"


class FreelMessage(models.Model):
    room = models.ForeignKey("chat.Room", on_delete=models.CASCADE, related_name="freel_messages")
    text = models.TextField(max_length=500)
    user = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name="freel_messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.user} {self.room})"
