from django.db import models
from apps.freelancer.models import Freelancer 
from apps.customer.models import Customer 
from apps.order.models import Order 


class FreelancerRating(models.Model):
    RATING_CHOICES = (
        (1, 'too bad'),
        (2, 'bad'),
        (3, 'normal'),
        (4, 'good'),
        (5, 'excellent')
    )

    freelancer = models.ForeignKey(Freelancer, related_name='ratings', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ['freelancer', 'customer']



class Favorite(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='favorites')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='favorite_freelancers')

    class Meta:
        unique_together = ['freelancer', 'customer']



class FreelCommentOrder(models.Model):
    freelancer = models.ForeignKey(Freelancer, related_name='f_comments_o', on_delete=models.CASCADE)
    comment = models.TextField()
    order = models.ForeignKey(Order, related_name='f_comments_o', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class FreelCommentCustomer(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='c_comments_f')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='c_comments_f')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




class CustCommentOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='c_comments_o')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='c_comments_o')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()



class CustCommentFreel(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='f_comments_c')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='f_comments_c')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

