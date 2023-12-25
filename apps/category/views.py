from django.shortcuts import render
from .models import Category
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework import permissions


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            return permissions.AllowAny(),
        return permissions.IsAdminUser(),

