from . import views 
from django.urls import path 

urlpatterns = [
    path('create/', views.CreateOrderAPIView.as_view(), name='create-order'),
    path('<int:pk>/accept/proposal/<int:freelancer>/', views.AcceptOrderView.as_view(), name='accept-order'),
    path('<int:pk>/freelancer/completed/', views.FreelCompleteOrderView.as_view(), name='freelancer-completed-order'),
    path('<int:pk>/customer/completed/', views.CustCompleteOrderView.as_view(), name='customer-completed-order'),
]