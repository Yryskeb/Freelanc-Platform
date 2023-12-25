from django.urls import path 
from . import views 
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('register_phone/', views.RegistrationPhoneView.as_view()),
    path('activate/', views.ActivationView.as_view()),
    path('activate_phone/', views.ActivationPhoneView.as_view()),
    path('login/', views.CustomerLoginView.as_view()), 
    path('refresh/', TokenRefreshView.as_view()),
    path('reset_password/', views.ResetPasswordAPIView. as_view()),
    path('reset/new/password/', views.ActivePasswordAPIView.as_view()),
]