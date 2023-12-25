from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from apps.freelancer.tasks import send_activation_sms, send_confirmation_email, reset_password
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet 
from rest_framework import permissions 
from apps.freelancer.serializers import FreelUserSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAuthor
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from apps.feedback.serializers import FreelancerRatingSerializer, FreelCommentCustomer, FreelCommentCustomerSerializer
from django.http import HttpResponseServerError
from apps.customer.models import Customer
from apps.freelancer.serializers import Freelancer
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
        user = get_object_or_404(Freelancer, activation_code=code)
        user.is_active = True 
        user.activation_code = ''
        user.save()
        return Response('Succesfuly activated', status=200)
    

class FreelancerLoginView(APIView):

    def post(self, request, *args, **kwargs):
        settings.AUTH_USER_MODEL = 'freelancer.Freelancer'

        try:
            freelancer = Freelancer.objects.get(email=request.data.get('email'), is_active=True)
        except Freelancer.DoesNotExist:
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if freelancer.check_password(request.data.get('password')):
            refresh = RefreshToken.for_user(freelancer)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({"access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ResetPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(Freelancer, email=email)

        if user:
            try:
                reset_password.delay(email)
            except:
                return Response({"error": "Email dose not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response({'success': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)
    

class ActivePasswordAPIView(APIView):
    def post(self, request):
        settings.AUTH_USER_MODEL = 'freelancer.Freelancer'

        email = request.data.get('email')
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
            freelancer = Freelancer.objects.get(email=email, is_active=True)
        except Freelancer.DoesNotExist:
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if password == password_confirm:
            refresh = RefreshToken.for_user(freelancer)
            access_token = str(refresh.access_token)
            freelancer.password = make_password(password)
            freelancer.save()
            
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
        user = Freelancer.objects.filter(phone_number=phone, activation_code=code).first()
        if not user:
            return Response('No such user', status=400)
        user.activation_code = ''
        user.is_active = True 
        user.save()
        return Response('Succesfuly activated', status=200)
    



class StandartPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class FreelancerViewSet(ModelViewSet):
    queryset = Freelancer.objects.all()
    serializer_class = FreelUserSerializer 
    pagination_class = StandartPagination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('profession', 'what_i_can', 'category', 'price', 'work_time', )
    filterset_fields = ('profession', 'price', 'city', 'category', 'price', 'work_time',)


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticatedOrReadOnly()]    
    
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def rating(self, request, pk):
        freelancer = self.get_object()
        user = request.user
        if not isinstance(user, Customer):
            return HttpResponseServerError("Ошибка: request.user не является экземпляром Customer.")

        if request.method == 'GET':
            ratings = freelancer.ratings.all()
            serializer = FreelancerRatingSerializer(instance=ratings, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if freelancer.ratings.filter(customer=user).exists():
                return Response('You already rated this freelancer', status=400)
            data = request.data
            serializer = FreelancerRatingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            freelancer_id = Freelancer.objects.get(id=pk)
            print(freelancer_id)
            serializer.save(customer=user, freelancer=freelancer_id)
            return Response(serializer.data, status=201)

        else:
            if not freelancer.ratings.filter(customer=user).exists():
                return Response("You didn't rated this freelancer")
            rating = freelancer.ratings.get(customer=user)
            rating.delete()
            return Response('Deleted', status=204)
        

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def cust_comments(self, request, pk):
        comments = FreelCommentCustomer.objects.filter(freelancer=request.user.id)

        if request.method == 'GET':
            serializer = FreelCommentCustomerSerializer(instance=comments, many=True)
            return Response(serializer.data, status=200)
        
        elif request.method == 'POST':
            data = request.data.copy()
            data['freelancer'] = request.user.id
            data['customer'] = pk
            serializer = FreelCommentCustomerSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)        

        else:
            comment_id = request.query_params.get('comment_id')
            if not comment_id:
                return Response({'error': 'comment_id parameter is required'}, status=400)
            
            try:
                comment = FreelCommentCustomer.objects.get(id=comment_id, freelancer=request.user.id)
                comment.delete()
                return Response('Deleted', status=204)
            except FreelCommentCustomer.DoesNotExist:
                return Response({'error': 'Comment not found'}, status=404)
    
    
    

@api_view(['GET'])
def get_hello(request):
    print(request.hello)
    return Response('Hello Ryu')