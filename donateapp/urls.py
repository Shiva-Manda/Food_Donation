from django.urls import path
from . import views

urlpatterns = [
    path('home_authenticated/', views.home_authenticated, name="home_authenticated"),
    path('', views.home, name='home'),
    path('health/',views.health_check),

    path('donare/', views.FoodDonareCreateView.as_view(), name="donare"),
    path('display_donare/', views.DonareDisplayView.as_view(), name="display_donare"),
    path('donare_detail/<int:pk>/', views.DonareDetailView.as_view(), name="donare_detail"),
    path('update_donare/<int:pk>/', views.DonareUpdateView.as_view(), name="update_donare"),
    path('delete_donare/<int:pk>/', views.DonareDeleteView.as_view(), name="delete_donare"),


    path('acceptor/', views.acceptor, name="acceptor"),
    path('search_food/', views.SearchResultsView.as_view(), name="search_food"),
    path("request/<int:donation_id>/", views.RequestView.as_view(), name="request"),
    path('notification/', views.NotificationView, name="notification"),


    path('signup/', views.signup_view, name="signup"),

    path("donor_notifications/", views.DonorNotificationView, name="donor_notifications"),
    path("received_requests/", views.received_requests, name="received_requests"),

]
