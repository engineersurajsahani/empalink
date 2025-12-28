from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm, UserProfileForm, VolunteerProfileForm
from .models import VolunteerProfile
from stories.models import Story
from donations.models import Donation

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin':
            return reverse_lazy('admin_dashboard')
        elif user.role == 'donor':
            return reverse_lazy('donor_dashboard')
        elif user.role == 'volunteer':
            return reverse_lazy('volunteer_dashboard')
        return reverse_lazy('home')


class SignUpView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration successful! Please login to continue.')
        return super().form_valid(form)


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        
        # Handle volunteer profile form if user is a volunteer
        if request.user.role == 'volunteer':
            volunteer_profile, created = VolunteerProfile.objects.get_or_create(user=request.user)
            volunteer_form = VolunteerProfileForm(request.POST, instance=volunteer_profile)
            
            if user_form.is_valid() and volunteer_form.is_valid():
                user_form.save()
                volunteer_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        
        # Handle volunteer profile form if user is a volunteer
        if request.user.role == 'volunteer':
            volunteer_profile, created = VolunteerProfile.objects.get_or_create(user=request.user)
            volunteer_form = VolunteerProfileForm(instance=volunteer_profile)
        else:
            volunteer_form = None
    
    context = {
        'user_form': user_form,
        'volunteer_form': volunteer_form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_view(request):
    # Redirect to appropriate dashboard based on user role
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'donor':
        return redirect('donor_dashboard')
    elif request.user.role == 'volunteer':
        return redirect('volunteer_dashboard')
    
    return render(request, 'accounts/dashboard.html')


@login_required
def donor_dashboard(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-donation_date')
    total_donated = sum(donation.amount for donation in donations)
    
    # Count donations by status
    confirmed_donations_count = donations.filter(status='confirmed').count()
    pending_donations_count = donations.filter(status='pending').count()
    
    context = {
        'donations': donations,
        'total_donated': total_donated,
        'confirmed_donations_count': confirmed_donations_count,
        'pending_donations_count': pending_donations_count,
    }
    return render(request, 'accounts/donor_dashboard.html', context)


@login_required
def volunteer_dashboard(request):
    if hasattr(request.user, 'volunteer_profile'):
        volunteer_profile = request.user.volunteer_profile
    else:
        volunteer_profile = None
    
    # Get stories created by this volunteer
    created_stories = Story.objects.filter(creator=request.user).order_by('-created_at')
    
    context = {
        'volunteer_profile': volunteer_profile,
        'created_stories': created_stories,
    }
    return render(request, 'accounts/volunteer_dashboard.html', context)


@login_required
def admin_dashboard(request):
    # Only accessible to admin users
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin access required.')
        return redirect('home')
    
    total_users = User.objects.count()
    total_stories = Story.objects.count()
    total_donations = Donation.objects.count()
    pending_stories = Story.objects.filter(status='pending').count()
    pending_donations = Donation.objects.filter(status='pending').count()
    
    context = {
        'total_users': total_users,
        'total_stories': total_stories,
        'total_donations': total_donations,
        'pending_stories': pending_stories,
        'pending_donations': pending_donations,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return HttpResponseRedirect(reverse_lazy('home'))