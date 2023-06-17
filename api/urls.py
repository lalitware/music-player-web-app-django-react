from django.urls import path
from . import views

urlpatterns = [
    path('room/', views.RoomView.as_view(), name='get_rooms'),
    path('create-room/', views.CreateRoomView.as_view(), name='create_room'),
    path('get-room/', views.GetRoom.as_view(), name='get_room'),
    path('join-room/', views.JoinRoom.as_view(), name='join_room'),
    path('user-in-room/', views.UserInRoom.as_view(), name='user_in_room'),
    path('leave-room/', views.LeaveRoom.as_view(), name='leave_room'),
    path('update-room/', views.UpdateRoom.as_view(), name='update_room'),
]