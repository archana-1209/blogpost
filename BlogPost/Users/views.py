from django.db import models
from django.contrib.auth.models import Group, PermissionsMixin,User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes,APIView
from rest_framework.response import Response
from .serializer import RegistrationSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseForbidden


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self,request):
    
        data = {}
        print("request_data",request.data)
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        account = serializer.save()
        password = serializer.validated_data["password"]
        account.set_password(password)           
        account.is_active = True
        account.save()
        token = Token.objects.get_or_create(user=account)[0].key
        data["message"] = "user registered successfully"
        data["email"] = account.email
        data["username"] = account.username
        data["token"] = token


        return Response(data)

#     except KeyError as e:
#         print(e)
#         raise ValidationError({"400": f'Field {str(e)} missing'})


class LoginView(APIView):
    permission_classes = [AllowAny]
    #authentication_classes = []
    
    def post(self,request):
            print("yes")
            data = {}
            email=request.data['email']
            password=request.data['password']
            
            try:

                Account = User.objects.get(email=email)
            except BaseException as e:
                return JsonResponse({
                'status': 400,
                'message': str(e)
            }, status=400)

            token = Token.objects.get_or_create(user=Account)[0].key
            if not Account.check_password(password):
                return JsonResponse({
                'status': 400,
                'message': 'Password is incorrect.'
            }, status=400)

            if Account:
                if Account.is_active:
                    login(request,Account)
                    data["message"] = "user logged in"
                    data["email_address"] = Account.email

                    Res = {"data": data, "token": token}

                    return Response(Res)

                else:
                     return JsonResponse({
                'status': 400,
                'message': 'Account not active'
            }, status=400)

            else:
                 return JsonResponse({
                'status': 400,
                'message': 'Account doesn"t exist'
            }, status=400)