from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:id>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updatedRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk_room>/<str:pk>/', views.deleteMessage, name='delete-message'),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('update-user/<str:pk>/', views.updateUser, name='update-user'),
    path('topic-page/', views.topicsPage, name='topics-page'),
    path('activities-page/', views.activitiesPage, name='activities-page'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
]
