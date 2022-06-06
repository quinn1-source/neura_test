from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
import dashboard.constants


User = get_user_model()

# Create your models here.
class ContactUsNotificationFile(models.Model):
    contact_us_target = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_us_from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="contact_us_from_user")
    contact_us_redirect_url = models.URLField(max_length=500, null=True, unique=False, blank=True, help_text="The URL to be visited when a notification is clicked.") #related_name="contact_us_redirect_url")
    contact_us_verb = models.CharField(max_length=255, unique=False, blank=True, null=True)
    read_time = models.DateTimeField(blank=True, null=True)
    contact_us_timestamp = models.DateTimeField(auto_now_add=True)
    contact_us_read = models.BooleanField(default=False)
    
    def __str__(self):
            return self.contact_us_verb

class ContactUsFile(models.Model):
    contact_us_message = models.CharField(max_length=500, blank=True, null=True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    read_unread = models.CharField(max_length=10, blank=True, null=True, default=False)
    read_time = models.DateTimeField(default=datetime.today, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    auto_id = models.AutoField(auto_created=True, primary_key=True)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    # notifications = GenericRelation(Notification)

