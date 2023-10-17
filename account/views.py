from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework.views import APIView


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
