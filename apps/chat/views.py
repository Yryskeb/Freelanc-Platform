from rest_framework.viewsets import ModelViewSet 
from apps.chat.models import Room, Customer
from apps.chat.serializers import RoomSerializer
from apps.chat.permissions import IsOwner
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

class StandartPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer 
    pagination_class = StandartPagination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('name', )
    filterset_fields = ('name', 'cust_host', 'freel_host')


    def perform_create(self, serializer):
        if isinstance(self.request.user, Customer):
            serializer.save(host=self.request.user)
        return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticatedOrReadOnly()]    
    