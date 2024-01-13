from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('edit/<id>/', views.changeInformation),
    path('profile/<id>/', views.changePicture),
    path('forget/<id>/', views.forgetPassword),
    path('change/<id>/', views.changePassword),
    path('verify/<id>/', views.verifyEmail)
]
