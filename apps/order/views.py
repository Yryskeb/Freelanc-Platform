from django.shortcuts import render
from apps.order.models import Order, Proposal
from apps.order.serializers import OrderSerializer, ProposalSerializer
from apps.order.permission import IsOwner

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView 
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import AnonymousUser

import logging 

from apps.customer.models import Customer
from apps.customer.serializers import CustUserSerializer 
from apps.freelancer.models import Freelancer
from apps.freelancer.serializers import FreelUserSerializer
from apps.feedback.serializers import FreelCommentOrder, FreelCommentOrderSerializer, CustCommentOrder, CustCommentOrderSerializer

logger = logging.getLogger(__name__)


class AcceptOrderView(APIView):
    def post(self, request, pk, freelancer):
        order = Order.objects.get(pk=pk, client=request.user)
        freelancer = Freelancer.objects.get(id=freelancer)
        
        if order == None:
            return Response('You are not the customer of this order', status=status.HTTP_403_FORBIDDEN)
        elif freelancer == None:
            return Response('Freelancer not found.', status=status.HTTP_404_NOT_FOUND)
        else:
            order.status = 'in_process'
            order.freelancer = freelancer
            proposal = Proposal.objects.get(freelancer=freelancer)
            proposal.is_accepted = True 
            order.budget = proposal.bid_amount
            order.save()
            proposal.save()

            response_data = {
                'order': OrderSerializer(order).data,
                'proposal': ProposalSerializer(proposal).data,
            }
        return Response(response_data, status=status.HTTP_200_OK)


class FreelCompleteOrderView(APIView):
    def post(self, request, pk):
        if isinstance(request.user, Freelancer):
            try:
                order = Order.objects.get(pk=pk, freelancer=request.user)
            except Order.DoesNotExist:
                return Response('Order not found or you are not the assigned freelancer.', status=status.HTTP_404_NOT_FOUND)
            
        else:
            return Response('Order not found or you are not the assigned freelancer.', status=status.HTTP_404_NOT_FOUND)

        if order.status != 'in_process':
            return Response('Cannot complete an order that is not in progress.', status=status.HTTP_400_BAD_REQUEST)
        order.freelancer_confirm = True 
        order.save()

        if order.client_confirm == True and order.freelancer_confirm == True:
            order.client.balance -= order.budget
            order.freelancer.balance += order.budget
            order.status = 'completed'
            order.save()
            order.client.save()
            order.freelancer.save()
        else:
            # response_data = {
            # 'order': OrderSerializer(order).data,
            # }
            return Response('You have completed the order. Wait until the customer confirms the completion of the order to receive payment.', status=status.HTTP_202_ACCEPTED)
                

class CustCompleteOrderView(APIView):
    def post(self, request, pk):
        if isinstance(request.user, Customer):
            try:
                order = Order.objects.get(pk=pk, client=request.user)
            except Order.DoesNotExist:
                return Response('Order not found or you are not the owner.', status=status.HTTP_404_NOT_FOUND)

        else:
            return Response('Order not found or you are not the owner.', status=status.HTTP_404_NOT_FOUND)

        if order.status != 'in_process':
            return Response('Cannot complete an order that is not in progress.', status=status.HTTP_400_BAD_REQUEST)
        order.client_confirm = True 
        order.save()

        if order.client_confirm == True and order.freelancer_confirm == True:
            order.client.balance -= order.budget
            order.freelancer.balance += order.budget
            order.status = 'completed'
            order.save()
            order.client.save()
            order.freelancer.save()

            return Response('You have confirmed the complation of your order. A certain amount specified in the order will be withdrawn from your balance.', status=status.HTTP_202_ACCEPTED)
        else:
            return Response('You have confirmed the complation of your order. A certain amount specified in the order will be withdrawn from your balance.', status=status.HTTP_202_ACCEPTED)


class StandartPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class ProposalViewSet(ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('freelancer', 'description', 'bid_amount', 'created_at')
    filterset_fields = ('bid_amount', 'freelancer', 'created_at', 'is_accepted')

    def perform_create(self, serializer):
        logger.info(self.request.user)
        if isinstance(self.request.user, Freelancer):
            serializer.save(freelancer=self.request.user)
        return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticatedOrReadOnly()] 
    

class CreateOrderAPIView(APIView):
    def post(self, request):
        balance = request.user.balance 
        budget = request.data.get('budget')
        print(float(balance) > float(budget))
        if float(balance) < float(budget):
            return Response('You do not have enough funds on your balance, you cannot create an order until you top up your balance.', status=status.HTTP_400_BAD_REQUEST)
        
        elif isinstance(request.user, Customer):
            serializer = OrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(client=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    pagination_class = StandartPagination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('freelancer', 'client', 'budget', 'title', 'description', 'created_at', 'category', 'deadline', 'status')
    filterset_fields = ('freelancer', 'client', 'budget', 'title', 'created_at', 'category', 'deadline', 'status')

    def perform_create(self, serializer):
        logger.info(self.request.user)

        if isinstance(self.request.user, Customer):
            serializer.save(client=self.request.user)
                  
        return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticatedOrReadOnly()]   
    
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def freel_comments(self, request, pk):
        order = self.get_object()
        comments = FreelCommentOrder.objects.filter(freelancer=request.user)

        if request.method == 'GET':
            serializer = FreelCommentOrderSerializer(instance=comments, many=True)
            return Response(serializer.data, status=200)
        
        elif request.method == 'POST':
            data = request.data.copy()
            data['order'] = order.id
            data['freelancer'] = request.user.id
            serializer = FreelCommentOrderSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)        

        else:
            comment_id = request.query_params.get('comment_id')
            if not comment_id:
                return Response({'error': 'comment_id parameter is required'}, status=400)
            
            try:
                comment = FreelCommentOrder.objects.get(id=comment_id, order=order)
                comment.delete()
                return Response('Deleted', status=204)
            except FreelCommentOrder.DoesNotExist:
                return Response({'error': 'Comment not found'}, status=404)
            
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def cust_comments(self, request, pk):
        order = self.get_object()
        comments = CustCommentOrder.objects.filter(customer=request.user)

        if request.method == 'GET':
            serializer = CustCommentOrderSerializer(instance=comments, many=True)
            return Response(serializer.data, status=200)
        
        elif request.method == 'POST':
            data = request.data.copy()
            data['order'] = order.id
            data['customer'] = request.user.id
            serializer = CustCommentOrderSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)        

        else:
            comment_id = request.query_params.get('comment_id')
            if not comment_id:
                return Response({'error': 'comment_id parameter is required'}, status=400)
            
            try:
                comment = CustCommentOrder.objects.get(id=comment_id, order=order)
                comment.delete()
                return Response('Deleted', status=204)
            except CustCommentOrder.DoesNotExist:
                return Response({'error': 'Comment not found'}, status=404)
    

    