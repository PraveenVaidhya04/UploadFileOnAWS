from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class AccountRegistrationSerializers(serializers.Serializer):
    username = serializers.CharField(style={"input_type": "text"}, write_only=True)
    email = serializers.CharField(style={"input_type": "text"}, write_only=True)
    first_name = serializers.CharField(style={"input_type": "text"}, write_only=True)
    last_name = serializers.CharField(style={"input_type": "text"}, write_only=True)
    password = serializers.CharField(style={"input_type": "text"}, write_only=True)

    def validate(self, data):
        username = data.get("username", "")
        email = data.get("email", "")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        password = data.get("password", "")

        if User.objects.filter(username=username).exists():
            mes = "Username already exist."
            raise exceptions.APIException(mes)

        elif User.objects.filter(email=email).exists():
            mes = "Email already exist."
            raise exceptions.APIException(mes)

        else:
            User_Info = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            User_Info.save()

            user_instance = get_object_or_404(User, email=email)
            user_instance.set_password(password)
            user_instance.save()

            return user_instance


class AccountLoginSerializers(serializers.Serializer):
    username = serializers.CharField(style={"input_type": "text"}, write_only=True)
    password = serializers.CharField(style={"input_type": "text"}, write_only=True)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if User.objects.filter(username=username).exists():
            user_instance = get_object_or_404(User, username=username)
            if user_instance.is_active:
                user = authenticate(username=username, password=password)
                if user is not None:
                    return user
                else:
                    mes = "Invalid login detail."
                    raise exceptions.APIException(mes)
            else:
                mes = "Account not activate."
                mes = {'detail': mes, 'active': False}
                raise exceptions.APIException(mes)
        else:
            mes = "Email not register."
            raise exceptions.APIException(mes)


