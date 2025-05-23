from django.urls import path
from . import views

urlpatterns = [
    path('workspaces/', views.WorkspaceListCreateView.as_view()),
    path('rooms/', views.ChatRoomListCreateView.as_view()),
    path('rooms/<int:room_id>/messages/', views.ChatMessageListCreateView.as_view()),
]
