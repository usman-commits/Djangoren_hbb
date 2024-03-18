from django.contrib import admin
from .models import Broadband, ReactivationReport, NccOutLet, UserProfile, UploadPhoto
from import_export.admin import ImportExportModelAdmin
from .resource import BroadbandResource
from django.utils.html import format_html
from django.conf import settings




@admin.register(Broadband)
class BroadbandModelAdmin(ImportExportModelAdmin):
    resource_class =  BroadbandResource
    list_display = ['id','HSE_name','Region','State','Device_type','MSISDN','IMEI','Alternate','Customer_name','Post_date']
    list_filter = ('Post_date',)
    date_hierarchy = 'Post_date'
    list_filter = ('Region', 'State','Post_date', 'Device_type')
    search_fields = ['HSE_name', 'State'] 


    class Media:
        css = {
            'all': (settings.STATIC_URL + 'admin/css/admin_page.css',)
        }
   

    

@admin.register(ReactivationReport)
class BroadbandModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['HSE_name','Total_calls','Successful_calls','Unsuccessful_calls','Successful_bundle','Post_date']
    list_filter = ('Post_date',)
    date_hierarchy = 'Post_date'

 
    class Media:
        css = {
            'all': (settings.STATIC_URL + 'admin/css/admin_page.css',)
        }


@admin.register(NccOutLet)
class BroadbandModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['HSE_name','Total_certified_outlet','Outlet_visited','Outlet_with_device','Total_devices_in_outlet','Total_devices_sold','Post_date']
    list_filter = ('Post_date',)
    date_hierarchy = 'Post_date'
    class Media:
        css = {
            'all': (settings.STATIC_URL + 'admin/css/admin_page.css',)
        }



@admin.register(UploadPhoto)
class UploadphotoAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'uploaded_photo', 'photo_caption']



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'uploaded_photo', 'avatar', 'date')
    search_fields = ('user__username', 'name')
    class Media:
        css = {
            'all': (settings.STATIC_URL + 'admin/css/admin_page.css',)
        }

    def display_uploaded_photo(self, obj):
        if obj.uploaded_photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.uploaded_photo.url)
        return '-'

    display_uploaded_photo.short_description = 'Uploaded Photo'

    def display_avatar(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.avatar.url) if obj.avatar else '')
    display_avatar.short_description = 'Avatar'

admin.site.site_header = 'HBB Data Administration'
admin.site.index_title = 'HBB Data Administration'





   

