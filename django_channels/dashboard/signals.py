import imp
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from dashboard.models import ContactUsFile


@receiver(post_save, sender=ContactUsFile)
def dashboard_create_notification(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    if created:
        print(list)
        helpdesk_user = Account.objects.get(username='helpdesk')
        print('user ', instance.user_name)
        print('helpdesk_user', helpdesk_user)
        if helpdesk_user == instance.user_name:
            target = helpdesk_user
            from_user = instance.user_name
        else:
            target = instance.user_name
            from_user = helpdesk_user
            target = instance.user_name

        instance.notifications.create(
			target = from_user,
			from_user = target,
			#redirect_url = "where to next??? URL for next template",
			verb = f"{instance.user_name} sent you an enquiry",
            content_type = content_type,
            object_id = 20           
		)

post_save.connect(dashboard_create_notification, sender=ContactUsFile)
