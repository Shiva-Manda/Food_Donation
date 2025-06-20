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
from django.http import HttpResponse
from .models import FoodAcceptor, FoodDonare, Notification
from .models import FoodAcceptor


def signup_view(request):
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
    context_object_name = 'donations'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if not query:
            return FoodDonare.objects.none()
        user = self.request.user
        donations = FoodDonare.objects.filter(address__icontains=query)
        donations = donations.exclude(user=user).exclude(requests__status="Accepted")
        return donations

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


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

        Notification.objects.create(
            user=donation.user,
            notification=f"{user.username} requested your donation: {donation.food_details[:20]}"
        )
        return super().form_valid(form)


@login_required
def NotificationView(request):
    notifications = Notification.objects.filter(user=request.user)
    requests = FoodAcceptor.objects.filter(donation__user=request.user, status="Pending")

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
                FoodAcceptor.objects.filter(donation=food_request.donation).exclude(id=food_request.id).update(status="Declined")
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

    return render(request, "donateapp/see_notification.html", {"notifications": notifications, "requests": requests})


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

def respond_to_request(request, request_id, action):
    pickup = get_object_or_404(FoodAcceptor, id=request_id)

    if action == 'accept':
        pickup.status = 'accepted'
        pickup.message = f"Your request for '{pickup.food.food_name}' was accepted. Donor contact: {pickup.donor.profile.phone_number}"  # Assuming phone is in profile
        messages.success(request, "You have accepted the request.")
    elif action == 'decline':
        pickup.status = 'declined'
        pickup.message = f"Your request for '{pickup.food.food_name}' was declined by the donor."
        messages.info(request, "You have declined the request.")

    pickup.save()
    return redirect('donor_dashboard')

def notifications_view(request):
    pickups = FoodAcceptor.objects.filter(acceptor=request.user).exclude(status='pending')
    requests = FoodAcceptor.objects.filter(donare__user=request.user, status='pending')

    return render(request, 'donateapp/notification.html', {
        'notifications': pickups,
        'requests': requests,
    })

