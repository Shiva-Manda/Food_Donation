from .models import Notification
from django.contrib.auth.models import AnonymousUser

def unread_notifications(request):
    if request.user == AnonymousUser() or not request.user.is_authenticated:
        return {}

    unread_count = Notification.objects.filter(user=request.user, is_seen=False).count()
    return {
        'unread_notifications_count': unread_count
    }
