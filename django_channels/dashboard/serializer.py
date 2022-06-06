from django.core.serializers.python import Serializer
from dashboard.models import ContactUsNotificationFile


class ContactUsNotificationFileEncoder(Serializer):
    
    def get_dump_object(self, obj):
        print(obj)
        print(str(obj.contact_us_target.username))

        dump_object = {}
        dump_object.update({'contact_us_target': str(obj.contact_us_target.username)})
        dump_object.update({'contact_us_from_user': str(obj.contact_us_from_user.username)})
        dump_object.update({'is_read': str(obj.contact_us_read)})
        dump_object.update({'contact_us_verb': str(obj.contact_us_verb)})
        dump_object.update({'contact_us_timestamp': str(obj.contact_us_timestamp)})
        #dump_object.update({'natural_timestamp': str(naturaltime(obj.timestamp))})
        dump_object.update({'contact_us_timestamp': str(obj.contact_us_timestamp)})
        dump_object.update({'contact_us_redirect_url': str(obj.contact_us_redirect_url)})
        dump_object.update({'id': int(obj.id)})
        
        
