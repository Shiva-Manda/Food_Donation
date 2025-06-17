from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
from datetime import timedelta

def default_expiry():
    return timezone.now() + timedelta(hours=5, minutes=30)



class FoodDonare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=12)
    address = models.CharField(max_length=400)
    food_details = models.TextField()
    donate_date = models.DateTimeField(default=timezone.now)

    prepared_time = models.DateTimeField(null=True, blank=True)
    expiry_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

    
class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name="notification", on_delete=models.CASCADE
    )
    notification = models.CharField(max_length=500, default=None)
    
class FoodAcceptor(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=12)
    any_message = models.TextField()
    donate_date = models.DateTimeField(default=timezone.now)
    donation = models.ForeignKey(FoodDonare, on_delete=models.CASCADE, related_name="requests", null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.status}"
