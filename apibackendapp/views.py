from django.shortcuts import render
from.models import employee,department,project,User,userdetails
from rest_framework import viewsets,filters
from .serializers import employeeserializer,departmentserializer,projectserializer,userserializer,userdetailsserializer,signupserializer,loginserializer
from rest_framework.views import APIView
#from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
# Create your views here.
# employeeviewset---->class name
#viewsets.modelviewset--->DRF class that provides implementations for CRUD operations
class employeeviewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    #collection of objects from the database using ORM
    queryset=employee.objects.all()
    serializer_class=employeeserializer
    #use the searchfilter functionality
    #searchfilter is built-in feauture provided by django

    filter_backends=[filters.SearchFilter]
    #specifies the fields in which the search should be performed
    search_fields=['EmployeeName','Designation']

class departmentviewset(viewsets.ModelViewSet):
    queryset=department.objects.all()
    serializer_class=departmentserializer

class projectviewset(viewsets.ModelViewSet):
    queryset=project.objects.all()
    serializer_class=projectserializer
# Create your views here.

class userviewset(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=userserializer

class userdetailsviewset(viewsets.ModelViewSet):
    queryset=userdetails.objects.all()
    serializer_class=userdetailsserializer

#class-based api-APIView is provided by djangorestframework
class signupapiview(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=signupserializer(data=request.data)
        if serializer.is_valid():
            #if the validation success,it will create a new user
            #DRF internally calls create() method inside the serializer
            user=serializer.save()
            #iftoken exists,returns the existing token,otherwise creates the new one
            #token,created=Token.objects.get_or_create(user=user)
            refresh=RefreshToken.for_user(user)
            return Response(
                {
                    "user_id":user.id,
                    "username":user.username,
                    "access":str(refresh.access_token),
                    "refresh":str(refresh),
                    #"token":token.key,
                    "role":user.groups.all()[0].id if user.groups.exists() else None
                },status=status.HTTP_201_CREATED
            )
        else:
            res={'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class loginapiview(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        #runs when POST/login is called
        #creates a serializer object and it receives the username and password from the frontend
        serializer=loginserializer(data=request.data) 
        #serializer will validate the data
        #it will check whether the username is present and password is present
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=authenticate(request,username=username,password=password)
            if user is not None:
                refresh=RefreshToken.for_user(user)
                #token=Token.objects.get(user=user)
                response={
                    "status":status.HTTP_200_OK,
                    "message":"success",
                    "username":user.username,
                    "access":str(refresh.access_token),
                    "refresh":str(refresh),
                    #"token":token.key,
                    "role":user.groups.all()[0].id if user.groups.exists() else None
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"invalid email or password",
                }
                return Response(response,status=status.HTTP_401_UNAUTHORIZED)
        response={
            "status":status.HTTP_400_BAD_REQUEST,
            "message":"bad_request",
            "data":serializer.errors
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST) 
