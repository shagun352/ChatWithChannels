
from django.urls import path
from .views import (
    UserRegisterView,
   LoginAPIView,
  
)

urlpatterns = [
    path('signup/', UserRegisterView.as_view()),
    path('login/', LoginAPIView.as_view()),

]
