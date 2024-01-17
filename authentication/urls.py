from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('edit/<id>/', views.changeInformation),
    path('profile/<id>/', views.changePicture),
    path('forget/', views.forgetPassword),
    path('change/', views.changePassword),
    path('verify/<id>/', views.verifyEmail)
]
