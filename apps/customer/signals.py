from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.customer.models import Customer
from django.db import IntegrityError
import random

@receiver(post_migrate)
def create_admin(sender, **kwargs):
    admin_email = 'admin@idea.com'
    area_code = random.randint(100, 999)
    remaining_digits = random.randint(1000000, 9999999)

    phone_number = f"{area_code}-{remaining_digits}"
    
    if not Customer.objects.filter(email=admin_email).exists() and not Customer.objects.filter(phone_number=phone_number).exists():
        Customer.objects.create_superuser(
            email=admin_email,
            password='admin@idea.com', 
            phone_number=phone_number,
        )


