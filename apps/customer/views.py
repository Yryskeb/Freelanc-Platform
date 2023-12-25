from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import permissions, status
from apps.customer.serializers import RegisterSerializer, CustUserSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from apps.customer.tasks import send_activation_sms, send_confirmation_email, reset_password
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAuthor
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer
from rest_framework.decorators import action
from apps.feedback.models import Favorite
from apps.feedback.serializers import FavoriteSerializer, CustCommentOrder, CustCommentFreel, CustCommentFreelSerializer, CustCommentOrderSerializer, FreelCommentCustomer, FreelCommentCustomerSerializer
from django.contrib.auth.hashers import make_password 
import uuid 


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serialier = RegisterSerializer(data=request.data)
        serialier.is_valid(raise_exception=True)
        user = serialier.save()
        if user:
            try:
                send_confirmation_email.delay(user.email, user.activation_code)
            except:
                return Response({'message': 'Registered, but troubles with email', 'data': serialier.data}, status=201)
        return Response(serialier.data, status=201)
    


class ActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(Customer, activation_code=code)
        user.is_active = True 
        user.activation_code = ''
        user.save()
        return Response('Succesfuly activated', status=200)
    

class CustomerLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            customer = Customer.objects.get(email=email, is_active=True)
        except Customer.DoesNotExist:
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if customer.check_password(password):
            refresh = RefreshToken.for_user(customer)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            settings.AUTH_USER_MODEL = 'customer.Customer'
            return Response({"access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email == None:
            return Response({'error': 'email field is required!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user:
            try:
                reset_password.delay(email)
            except:
                return Response({"error": "Email dose not exist."}, status=status.HTTP_404_NOT_FOUND)


        return Response({'success': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)
    

class ActivePasswordAPIView(APIView):
    def post(self, request):
        make_sure = request.query_params.get('make_sure')
        namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
        email = request.data.get('email')
        sure = uuid.uuid3(namespace, email)
        
        if make_sure != str(sure):
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_404_NOT_FOUND)
        password = request.data.get('password')
        password_confirm = request.data.get('password_confirm')  
        if email==None or password==None or password_confirm==None:
            return Response('Bad request! email, password, password_confirm is required!', status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(email=email, is_active=True)
        except Customer.DoesNotExist:
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if password == password_confirm:
            refresh = RefreshToken.for_user(customer)
            access_token = str(refresh.access_token)
            customer.password = make_password(password)
            
            customer.save()
            
            return Response({"access_token": access_token, 'new_password': password}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)




class RegistrationPhoneView(GenericAPIView):
    serializer_class = RegisterSerializer 

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_sms.delay(user.phone_number, user.activation_code)
            return Response('Seccsefully registered', status=201)
        

class ActivationPhoneView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = Customer.objects.filter(phone_number=phone, activation_code=code).first()
        if not user:
            return Response('No such user', status=400)
        user.activation_code = ''
        user.is_active = True 
        user.save()
        return Response('Succesfuly activated', status=200)
    



class StandartPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustUserSerializer 
    pagination_class = StandartPagination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('balance', )
    filterset_fields = ('balance', )


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticatedOrReadOnly()]    
    

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def favorites(self, request, pk=None):
        if request.method == 'GET':
            favorites = Favorite.objects.filter(customer_id=pk)
            serializer = FavoriteSerializer(instance=favorites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            user = request.user
            favorite_data = {'freelancer': pk, 'customer': user.id}
            serializer = FavoriteSerializer(data=favorite_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user = request.user  
            favorite = Favorite.objects.filter(freelancer_id=pk, customer=user).first()
            if favorite:
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)
    

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def freel_comments(self, request, pk):
        comments = CustCommentFreel.objects.filter(customer=request.user.id)

        if request.method == 'GET':
            serializer = CustCommentFreelSerializer(instance=comments, many=True)
            return Response(serializer.data, status=200)
        
        elif request.method == 'POST':
            data = request.data.copy()
            data['customer'] = request.user.id
            data['freelancer'] = pk
            serializer = CustCommentFreelSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)        

        elif request.method == 'DELETE':
            comment_id = request.query_params.get('comment_id')
            if not comment_id:
                return Response({'error': 'comment_id parameter is required'}, status=400)
            
            try:
                comment = CustCommentFreel.objects.get(id=comment_id, customer=request.user.id)
                comment.delete()
                return Response('Deleted', status=204)
            except CustCommentFreel.DoesNotExist:
                return Response({'error': 'Comment not found'}, status=404)
