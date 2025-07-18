from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from donateapp import views as donate_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('donateapp.urls')),
 

   
    path('login/', auth_views.LoginView.as_view(template_name='donateapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home_not_authenticated'), name='logout'),
    path('signup/', donate_views.signup_view, name='signup'),

    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='donateapp/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='donateapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='donateapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='donateapp/password_reset_complete.html'), name='password_reset_complete'),
]

