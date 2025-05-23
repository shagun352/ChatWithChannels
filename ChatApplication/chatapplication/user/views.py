from rest_framework.views import APIView
from rest_framework import status

from .serializers import (
    UserRegisterSerilaizer,
    LoginSerializer, 
)
from .response import ResponseHandler

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerilaizer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return ResponseHandler.success(
                message='User Register Successfully',
                status_code=status.HTTP_200_OK,
                data=data
            )
        return ResponseHandler.error(
            message='Verification failed',

            status_code=status.HTTP_400_BAD_REQUEST,
            details=serializer.errors
        )
    

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return ResponseHandler.success(
                message="Login successful",
                status_code=200,
                data=data

            )
        return ResponseHandler.error(
            message="Validation error",
            status_code=400,
            details=serializer.errors
        )