from django.db import models
from apps.customer.models import Customer
from apps.freelancer.models import Freelancer 
from apps.category.models import Category


class OrderStatus(models.TextChoices):
    opened = 'opened'
    in_process = 'in_process'
    completed = 'completed'


    
class Order(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    desc_images = models.ImageField(upload_to='descr_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='client_orders')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.SET_NULL, null=True, blank=True, related_name='freelancer_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.opened)
    client_confirm = models.BooleanField(default=False)
    freelancer_confirm = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.id}. ({self.client} -- {self.title})'


class Proposal(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='proposals')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    description = models.TextField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.id}. ({self.freelancer} --> {self.order})'