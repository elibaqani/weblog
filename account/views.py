from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import  User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    "data": serializer.errors,
                    "message": "someting went wrong"
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                "data": {},
                "message": "your acount is created"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
          print(e)
          return Response({
              "data":{},
              "message":"something went wrong",
          },status=status.HTTP_400_BAD_REQUEST)

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

class LoginView(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    "data":serializer.errors,
                    "message":"someting went wrong"
                },status=status.HTTP_400_BAD_REQUEST)

            response= serializer.get_jwt_token(serializer.data)
            return Response (response,status= status.HTTP_200_OK)

        except Exception as e:
          print(e)
          return Response({
              "data":{},
              "message":"something went wrong",
          },status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        user = User.objects.filter(id=payload['id']).first()
        return Response({
            'data': UserSerializer(user).data,
            'message': 'User profile retrieved successfully',
            'status': status.HTTP_200_OK
        })

    def put(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']

            user = User.objects.filter(id=user_id).first()
            if not user:
                raise AuthenticationFailed('User not found')

            if 'username' in request.data:
                new_username = request.data['username']
                check_new_username = User.objects.filter(username=new_username).first()
                if check_new_username :
                    raise AuthenticationFailed('Username is exist already')
                else:
                   user.username = new_username

            if 'email' in request.data:
                new_email = request.data['email']
                user.email = new_email

            if 'password' in request.data:
                new_password = request.data['password']
                user.set_password(new_password)

            user.save()

            return Response({
                'data': UserSerializer(user).data,
                'message': 'User profile updated successfully',
                'status': status.HTTP_200_OK
            })
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')