from django.urls import path
from .import views

app_name ='accounts'

urlpatterns =[
    path('register-chef/',views.register_chef,name='register-chef'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout')
]