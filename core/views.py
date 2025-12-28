from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Notification
from stories.models import Story, Category
from donations.models import Donation

User = get_user_model()


def home(request):
    # Show approved stories on home page
    approved_stories = Story.objects.filter(status='approved').order_by('-created_at')[:6]  # Show latest 6
    categories = Category.objects.all()
    
    context = {
        'approved_stories': approved_stories,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)


@login_required
def transparency_dashboard(request):
    # Show transparency metrics
    total_donations = Donation.objects.filter(status='confirmed').count()
    total_donated = sum(donation.amount for donation in Donation.objects.filter(status='confirmed'))
    total_stories = Story.objects.filter(status='approved').count()
    total_donors = User.objects.filter(role='donor', donations__status='confirmed').distinct().count()
    
    # Get approved stories for the impact metrics section
    approved_stories = Story.objects.filter(status='approved').order_by('-created_at')
    
    context = {
        'total_donations': total_donations,
        'total_donated': total_donated,
        'total_stories': total_stories,
        'total_donors': total_donors,
        'approved_stories': approved_stories,
    }
    return render(request, 'core/transparency_dashboard.html', context)


@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Mark all as read
    user_notifications.update(is_read=True)
    
    context = {
        'notifications': user_notifications,
    }
    return render(request, 'core/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    # Redirect back to where user came from or to notifications page
    referer = request.META.get('HTTP_REFERER', 'notifications')
    return redirect(referer)
