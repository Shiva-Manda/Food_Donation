from django.urls import path
from . import views
from .views import RequestView
from donateapp.views import apply_migrations

urlpatterns = [
    
    path('', views.home_not_authenticated, name='home_not_authenticated'),
    path('migrate/', apply_migrations, name='apply_migrations'),
    path('home_authenticated/', views.home_authenticated, name="home_authenticated"),
    path('donare/', views.FoodDonareCreateView.as_view(), name="donare"),
    path('display_donare/', views.DonareDisplayView.as_view(), name="display_donare"),
    path('donare_detail/<int:pk>/', views.DonareDetailView.as_view(), name="donare_detail"),
    path('update_donare/<int:pk>/', views.DonareUpdateView.as_view(), name="update_donare"),
    path('delete_donare/<int:pk>/', views.DonareDeleteView.as_view(), name="delete_donare"),


    path('acceptor/', views.acceptor, name="acceptor"),
    path('search_food/', views.SearchResultsView.as_view(), name="search_food"),
    path("request-food/<int:donation_id>/", RequestView.as_view(), name="request_food"),
    path('notification/', views.NotificationView, name="notification"),


    path('signup/', views.signup_view, name="signup"),
    path('about_us/', views.about_us, name='about_us'),
    path("donor_notifications/", views.DonorNotificationView, name="donor_notifications"),
    path("received_requests/", views.received_requests, name="received_requests"),

]
