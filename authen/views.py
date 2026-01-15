from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.models import Group
from django.db.models import Q

from utils.renderers import UserRenderers
from utils.permissions import IsLogin
from utils.util import Util
from utils.response import (success_response,
                            success_created_response,
                            user_not_found_response,
                            bad_request_response
                        )

from authen.models import CustomUser
from authen.serializers import  (UserGroupsSerializer,
                                 UserRegisterSerializer, 
                                 UserLoginSerializer, 
                                 UserInformationSerializer, 
                                 UserUpdateSerializer, 
                                 UserChangePasswordSerializer,
                                 ResetPasswordSerializer,
                                 PasswordResetCompleteSerializer,
                                )



def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserGroupsView(APIView):
    """ User Groups Filter """

    @swagger_auto_schema(tags=['Auth'], responses={200: UserGroupsSerializer(many=True)})
    def get(self, request):
        instance = Group.objects.filter(Q(name='buyer') | Q(name='salesman'))
        serializer = UserGroupsSerializer(request.user, context={"request": request})
        return success_response(serializer.data)


class UserRegisterView(APIView):
    """ User Regsiter View """

    @swagger_auto_schema(tags=['Auth'], request_body=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instanse = serializer.save()
            tokens = get_token_for_user(instanse)
            return success_created_response(tokens)


class UserLoginView(APIView):
    """ User Login View """

    @swagger_auto_schema(tags=['Auth'], request_body=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            username = request.data["username"]
            password = request.data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                tokens = get_token_for_user(user)
                return success_created_response(tokens)
            else:
                return user_not_found_response("This user is not available to the system")
        return success_created_response(serializer.errors)


class UserProfileView(APIView):
    """ User Information, Update And Delete View """

    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=['Auth'], responses={200: UserInformationSerializer(many=True)})
    def get(self, request):
        serializer = UserInformationSerializer(request.user, context={"request": request})
        return success_response(serializer.data)
    
    @swagger_auto_schema(tags=['Auth'], request_body=UserUpdateSerializer)
    def put(self, request, *args, **kwarg):
        queryset = get_object_or_404(CustomUser, id=request.user.id)
        serializer = UserUpdateSerializer(context={"request": request}, instance=queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    @swagger_auto_schema(tags=['Auth'], responses={204:  'No Content'})
    def delete(self, request):
        user_delete = CustomUser.objects.get(id=request.user.id)
        user_delete.delete()
        return success_response("delete success")


@api_view(["POST"])
@swagger_auto_schema(
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='old_password'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='new_password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='confirm_password'),
            }
        )
    )
@permission_classes([IsAuthenticated])
@permission_classes([IsLogin])
def change_password(request):
    if request.method == "POST":
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get("old_password")):
                user.set_password(serializer.data.get("new_password"))
                user.save()
                update_session_auth_hash(request, user)
                return success_response("Password changed successfully.")
            return bad_request_response("Incorrect old password.")
        return bad_request_response(serializer.errors)


class RequestPasswordRestEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(tags=['Forget Password'], request_body=ResetPasswordSerializer)
    @action(methods=['post'], detail=False)
    def post(self, request):
        email = request.data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            absurl = f"http://localhost:5173/reset-password/{uidb64}/{token}"
            email_body = f"Hi \n Use link below to reset password \n link: {absurl}"
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your password",
            }

            Util.send(data)

            return success_response("We have sent you to rest your password")
        return user_not_found_response("This email is not found.")



class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetCompleteSerializer

    @swagger_auto_schema(tags=['Forget Password'], request_body=PasswordResetCompleteSerializer)
    @action(methods=['patch'], detail=False)
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response("success.")
    

class UserGetView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=['Auth'], responses={200: UserInformationSerializer(many=True)})
    def get(self, request, pk):
        instance = CustomUser.objects.filter(id=pk)
        serializer = UserInformationSerializer(instance, many=True, context={"request": request})
        return success_response(serializer.data)