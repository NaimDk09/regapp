from django.urls import path
from register.views import register, login_view, home_view, delete_user

urlpatterns = [
    path('register/', register, name='register' ),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('delete/<int:id>', delete_user, name='delete_user')
    
]
