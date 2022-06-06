from django.contrib import admin
from dashboard.models import ContactUsFile, ContactUsNotificationFile
# Register your models here.

class ContactUsFileAdmin(admin.ModelAdmin):
	#list_display = ['id','user_name', 'contact_us_message']
	#search_fields = ['id', 'user_name__username', 'user_name__email']
	#readonly_fields = ['id',]

	class Meta:
		model = ContactUsFile


admin.site.register(ContactUsFile, ContactUsFileAdmin)


class ContactUsNotificationFileAdmin(admin.ModelAdmin):
	list_display = ['id', 'contact_us_target', 'contact_us_from_user', 'contact_us_timestamp']
	search_fields =  ['contact_us_target', 'contact_us_from_user', 'contact_us_timestamp']  #['id',
	
	readonly_fields = ['id',]

	class Meta:
		model = ContactUsNotificationFile


admin.site.register(ContactUsNotificationFile, ContactUsNotificationFileAdmin)

