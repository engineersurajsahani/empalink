from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Story, Category
from .forms import StoryForm, StoryApprovalForm
from accounts.models import User


@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            story = form.save(commit=False)
            story.creator = request.user
            story.save()
            messages.success(request, 'Story created successfully! It will be reviewed by admin.')
            return redirect('my_stories')
    else:
        form = StoryForm(user=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'stories/create_story.html', context)


@login_required
def my_stories(request):
    stories = Story.objects.filter(creator=request.user).order_by('-created_at')
    
    context = {
        'stories': stories,
    }
    return render(request, 'stories/my_stories.html', context)


@login_required
def story_list(request):
    # Only show approved stories
    stories = Story.objects.filter(status='approved').order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        stories = stories.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        stories = stories.filter(category__name=category)
    
    # Filter by location (if we add location to the model later)
    location = request.GET.get('location')
    if location:
        # For now, we don't have location in the model, so this would be a placeholder
        pass
    
    # Pagination
    paginator = Paginator(stories, 10)  # Show 10 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'stories/story_list.html', context)


def story_detail(request, pk):
    # Get the story but only allow access to approved stories for non-admins
    story = get_object_or_404(Story, pk=pk)
    
    # Allow access if the story is approved OR if the user is an admin
    if story.status != 'approved' and request.user.role != 'admin':
        messages.error(request, 'Access denied. This story is not approved yet.')
        return redirect('story_list')
    
    context = {
        'story': story,
    }
    return render(request, 'stories/story_detail.html', context)


@login_required
def admin_story_approval(request):
    # Only accessible to admin users
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin access required.')
        return redirect('home')
    
    pending_stories = Story.objects.filter(status='pending').order_by('-created_at')
    
    context = {
        'pending_stories': pending_stories,
    }
    return render(request, 'stories/admin_story_approval.html', context)


@login_required
def approve_story(request, pk):
    # Only accessible to admin users
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin access required.')
        return redirect('home')
    
    story = get_object_or_404(Story, pk=pk)
    
    if request.method == 'POST':
        form = StoryApprovalForm(request.POST, instance=story)
        if form.is_valid():
            old_status = story.status  # Store old status before saving
            form.save()
            
            # Create a notification for the story creator
            from core.models import Notification
            notification_title = f"Story Status Updated: {story.title}"
            if story.status == 'approved':
                notification_message = f"Your story '{story.title}' has been approved and is now visible to donors."
            elif story.status == 'rejected':
                notification_message = f"Unfortunately, your story '{story.title}' has been rejected. Please contact admin for more information."
            else:
                notification_message = f"The status of your story '{story.title}' has been updated to {story.get_status_display()}."
            
            Notification.objects.create(
                recipient=story.creator,
                notification_type='story_approval',
                title=notification_title,
                message=notification_message,
                related_story=story,
            )
            
            messages.success(request, f'Story status updated to {story.get_status_display()}.')
            return redirect('admin_story_approval')
    else:
        form = StoryApprovalForm(instance=story)
    
    context = {
        'form': form,
        'story': story,
    }
    return render(request, 'stories/approve_story.html', context)
