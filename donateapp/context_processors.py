from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        return {'noti_count': Notification.objects.filter(user=request.user).count()}
    return {'noti_count': 0}
