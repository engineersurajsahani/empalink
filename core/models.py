from django.db import models
from accounts.models import User
from stories.models import Story
from donations.models import Donation


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('story_approval', 'Story Approval'),
        ('donation_confirmation', 'Donation Confirmation'),
        ('campaign_completion', 'Campaign Completion'),
        ('general', 'General Notification'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_story = models.ForeignKey(Story, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    related_donation = models.ForeignKey(Donation, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title} - {self.recipient.username}'
