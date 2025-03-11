# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .forms import CustomPasswordResetForm # Import CustomPasswordResetForm


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm # Use our custom form

    def send_mail(self, subject, message, from_email, recipient_list, **kwargs):
        kwargs['html_message'] = kwargs.pop('html_message', message)
        super().send_mail(subject, message, from_email, recipient_list, **kwargs)


def register(request):
    if request.method == "POST":
        # Get form data from POST
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # Simple validation: check if passwords match
        if password != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "accounts/register.html")
        
        # Optionally check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "accounts/register.html")
        
        # Create the user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            # messages.success(request, "User created successfully")
            # Optionally, log the user in immediately:
            login(request, user)
            return redirect("search")  # Redirect to a home page (change URL name as needed)
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return render(request, "accounts/register.html")
    else:
        return render(request, "accounts/register.html")

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("search")  # Redirect after successful login
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "accounts/login.html")
    else:
        return render(request, "accounts/login.html")
