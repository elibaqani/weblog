from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class RegisterSerializer(serializers.Serializer):
    first_name =serializers.CharField()
    last_name =serializers.CharField()
    username =serializers.CharField()
    password =serializers.CharField()

    def validate(self,data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("user is taken")
        return data

    def create(self, validated_data):
       user = User.objects.create(first_name = validated_data["first_name"],last_name = validated_data["last_name"],username = validated_data["username"].lower(),
                                  password =validated_data['password'])
       # user.set_password(validated_data['password'])
       user.save()
       return validated_data

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('account not found')
        return data

    def get_jwt_token(self,data):
        user = User.objects.filter(username=data["username"]).first()
        # user = authenticate(username=data['username'],password=data['password'])
        if not user:
            return {
                "message":"invalid credevtials",
                "data" : {}
            }
        # if not user.check_password(data["password"]):
        if user.password != data["password"]:
            return {
                "message": "invalid password",
                "data": {}
            }

        refresh =RefreshToken.for_user(user)
        return {'message':"login success","token":str(refresh)}
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        # }}}