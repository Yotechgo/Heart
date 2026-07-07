from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('predict/', views.predict_heart_disease, name='predict_heart_disease'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
]