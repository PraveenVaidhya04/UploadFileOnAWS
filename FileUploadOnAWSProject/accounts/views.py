from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
# from imratedme.tokens import CsrfExemptSessionAuthentication
from django.contrib.auth import login
from django.contrib.auth.models import User
from .serializer import AccountRegistrationSerializers, AccountLoginSerializers
from django.contrib.auth import logout


# Create class for account registration.
class AccountRegistrationView(APIView):
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = AccountRegistrationSerializers(request,
                                                        data=request.data)  # Call serializer function for registration.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                data['detail'] = "Registration successfully"  # Response as a successful message.
                data['status'] = 1
                data['user_id'] = serializer.validated_data.id
            return Response(data)  # Send response as a API result.


class AccountLoginView(APIView):

    # Create function for post method.
    def post(self, request):
        if request.method == "POST":  # Check method is post or not.
            serializer = AccountLoginSerializers(request, data=request.data)  # Call serializer function for login.
            data = {}
            if serializer.is_valid():  # Get data if serializer is valid.
                login(request, serializer.validated_data)  # Login function.
                user_instance = get_object_or_404(User, pk=serializer.validated_data.id)
                if Token.objects.filter(user=user_instance).exists():
                    token = get_object_or_404(Token, user=user_instance)
                else:
                    token = Token.objects.create(user=serializer.validated_data)

                data['detail'] = "Logged in successfully"  # Response as a successful message.
                data['status'] = 1
                data['token'] = str(token)
                data['user_id'] = str(serializer.validated_data.id)  # Get user id from serializer response.
            return Response(data)  # Send response as a API result.


class Logout(APIView):
    def get(self, request):
        data = {}
        logout(request)
        data['detail'] = "Logged out successfully"
        data['status'] = 1
        return Response(data)
