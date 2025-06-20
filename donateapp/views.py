from datetime import date
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import FoodAcceptor, FoodDonare, Notification
from .forms import FoodRequestForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.http import HttpResponse



@csrf_exempt
def health_check(request):
    call_command("migrate")
    return HttpResponse("Migration Done")
def signup_view(request):
    try:
        
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Account created successfully!")
                return redirect('home_authenticated')
        else:
            form = UserCreationForm()
        return render(request, 'donateapp/signup.html', {'form': form})
    except Exception as e:
        return HttpResponse(f"Error occurred: {e}")
def about_us(request):
    return render(request, 'donateapp/about_us.html')
@login_required
def home_authenticated(request):
    return render(request, 'donateapp/home_authenticated.html')
def home_not_authenticated(request):
    return render(request, 'donateapp/home_not_authenticated.html')
class FoodDonareCreateView(SuccessMessageMixin, CreateView):
    model = FoodDonare
    template_name = 'donateapp/donare.html'
    fields = ["contact_number", "address", "food_details"]
    success_url = reverse_lazy("donare")
    success_message = "Donation information saved successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DonareDisplayView(ListView):
    model = FoodDonare
    template_name = "donateapp/donare_display.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["donare"] = FoodDonare.objects.filter(user=self.request.user)
        return context

class DonareDetailView(DetailView):
    model = FoodDonare
    context_object_name = 'donare'
    template_name = "donateapp/donare_detail.html"

class DonareUpdateView(SuccessMessageMixin, UpdateView):
    model = FoodDonare
    template_name = "donateapp/donare_update.html"
    fields = ["contact_number", "address", "food_details"]
    success_url = reverse_lazy("display_donare")
    success_message = "Donation updated successfully."

class DonareDeleteView(SuccessMessageMixin, DeleteView):
    model = FoodDonare
    template_name = "donateapp/donare_delete.html"
    success_url = reverse_lazy("display_donare")
    success_message = "Donation deleted successfully."

def acceptor(request):
    return render(request, 'donateapp/acceptor.html')

class SearchResultsView(ListView):
    model = FoodDonare
    template_name = "donateapp/acceptor.html"
    FoodDonare.objects.filter(
    expiry_time__gt=now()
    )

    def get_queryset(self):
        query = self.request.GET.get("q")
        donations = FoodDonare.objects.filter(address__icontains=query)
        donations = donations.exclude(requests__status="Accepted")
        return donations


class RequestView(CreateView):
    model = FoodAcceptor
    template_name = 'donateapp/request.html'
    fields = ["contact_number", "any_message"]
    
    def get_success_url(self):
        return reverse_lazy("home_authenticated")

    def form_valid(self, form):
        user = self.request.user
        donation_id = self.kwargs.get('donation_id')  
        donation = get_object_or_404(FoodDonare, id=donation_id)

        form.instance.user = user
        form.instance.donation = donation
        form.instance.status = "Pending"
        form.save()

        
        notif_msg = f"{user.username} requested your donation: {donation.food_details[:20]}"
        notif = Notification(user=donation.user, notification=notif_msg)
        notif.save()

        return super().form_valid(form)


def NotificationView(request):
    notifications = Notification.objects.filter(user=request.user)
    requests = FoodAcceptor.objects.filter(
        donation__user=request.user, status="Pending"
    )

    if request.method == "POST":
        
        if 'request_id' in request.POST:
            request_id = request.POST.get("request_id")
            action = request.POST.get("action")

            try:
                food_request = FoodAcceptor.objects.get(id=request_id)
            except FoodAcceptor.DoesNotExist:
                messages.error(request, "Request not found.")
                return redirect("notification")

            if action == "accept":
                food_request.status = "Accepted"
                food_request.save()

              
                Notification.objects.create(
                    user=food_request.user,
                    notification=f"Your food request has been accepted! Donor Contact: {food_request.donation.contact_number}"
                )

                
                FoodAcceptor.objects.filter(
                    donation=food_request.donation
                ).exclude(id=food_request.id).update(status="Declined")

                messages.success(request, "Request accepted successfully.")

            elif action == "decline":
                food_request.status = "Declined"
                food_request.save()

                Notification.objects.create(
                    user=food_request.user,
                    notification="Your food request was declined by the donor."
                )

                messages.info(request, "Request declined.")

        else:
            
            notifications.delete()
            messages.success(request, "Notifications cleared.")

        return redirect("notification")

    return render(
        request,
        "donateapp/see_notification.html",
        {"notifications": notifications, "requests": requests}
    )
@login_required
def DonorNotificationView(request):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        
        try:
            food_request = FoodAcceptor.objects.get(id=request_id, donation__user=request.user)
            if action == "accept":
                food_request.status = "Accepted"
                msg = f"Your request for donation by {food_request.donation.user.username} was accepted."
            elif action == "decline":
                food_request.status = "Declined"
                msg = f"Your request for donation by {food_request.donation.user.username} was declined."
            else:
                msg = None

            if msg:
                food_request.save()
                
                Notification.objects.create(user=food_request.user, notification=msg)
                messages.success(request, f"Request {action}ed successfully.")

        except FoodAcceptor.DoesNotExist:
            messages.error(request, "Request not found or you are not authorized.")

    
    requests = FoodAcceptor.objects.filter(donation__user=request.user, status="Pending")
    return render(request, 'donateapp/donor_notifications.html', {'requests': requests})




@login_required
def received_requests(request):

    donations = FoodDonare.objects.filter(user=request.user)

    food_requests = FoodAcceptor.objects.filter(donation__in=donations, status='Pending')

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        food_request = FoodAcceptor.objects.get(id=request_id)
        if action == 'accept':
            food_request.status = 'Accepted'
            Notification.objects.create(
                user=food_request.user,
                notification=f"Your request for {food_request.donation.food_details} was accepted."
            )
        elif action == 'decline':
            food_request.status = 'Declined'
            Notification.objects.create(
                user=food_request.user,
                notification=f"Your request for {food_request.donation.food_details} was declined."
            )
        food_request.save()
        return redirect('received_requests')

    return render(request, 'donateapp/received_requests.html', {'requests': food_requests})
