from .models import FoodAcceptor, Notification

def notification_count(request):
    if request.user.is_authenticated:
        donor_count = FoodAcceptor.objects.filter(donation__user=request.user, status="Pending").count()
        acceptor_count = Notification.objects.filter(user=request.user).count()
        return {"donor_notification_count": donor_count, "acceptor_notification_count": acceptor_count}
    return {}
