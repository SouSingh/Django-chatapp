from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="Home" ),
    path('room/<str:pk>', views.room, name="room" ),
    path('create-room/', views.createRoom, name="create_room"),
    path('update-room/<str:pk>', views.updateRoom, name="update_room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete_room"),
    path('user-profile/<str:pk>', views.userProfile, name="user_profile"),
    path('loginuser/', views.loginPage, name="login_page"),
    path('logout/', views.logoutuser, name="logout_fun"),
    path('register/', views.registerpage, name="register_page"),
    path('delete-message/<str:pk>', views.deleteMessage, name="Delete_page"),
    path('createtopic', views.createTopic, name="Createttopic")
]