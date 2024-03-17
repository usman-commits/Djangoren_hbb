from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.contrib.auth import views as auth_views
from . views import (
                    logout_view, 
                    DeviceRegistrationView,
                    ProfileView, 
                    DeleteProfilePictureView, 
                    PhotoUploadView, PhotoView, 
                    post_or_delete_photo, 
                    dynamic_pie_charts, 
                    export_pie_data, 
                    RegionView, 
                    StateView, 
                    UserDetailsView, 
                    BroadbandTabView, 
                    populate_table, 
                    populate_table, 
                    populate_default_table,
                    ResetDataView, get_combined_table_data,
                    get_current_date_time, 
                    get_all_states_table_data
) 
from .forms import(
                LoginForm, 
                DeviceRegistrationForm, 
                MyPasswordChangeForm, 
                MyPasswordResetForm, 
                MySetPasswordForm
) 



urlpatterns = [
     path('', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm, success_url='home/'), name='login'),
    path('home/',views.DeviceRegistrationView.as_view(), name='home'),
    path('reactivationreport/',views.ReactivationReportView.as_view(), name='reactivationreport'),
    path('nccoutlet/',views.NccOutLetView.as_view(), name='nccoutlet'),
    path('registration/', views.StaffRegistrationView.as_view(), name='staffregistration'), 
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('fetch_data/', views.ExportDataView.as_view(), name='fetch_data'),
    path('generate_region_data/', views.generate_region_data, name='generate_region_data'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete_profile_picture/', DeleteProfilePictureView.as_view(), name='delete_profile_picture'),
    path('upload/', PhotoUploadView.as_view(), name='upload_photo'),
    path('view/', PhotoView.as_view(), name='view_photo'),
    path('post_or_delete/', post_or_delete_photo, name='post_or_delete_photo'),
    path('pie_chart/', dynamic_pie_charts, name='pie_chart'),
    path('export_pie_data/', export_pie_data, name='export_pie_data'),
    path('get_all_states_table_data/', get_all_states_table_data, name='get_all_states_table_data'),
   
   
    path('region/<str:region>/', RegionView.as_view(), name='region_view'),
    path('state/<str:state>/', StateView.as_view(), name='state_view'),
    path('user-details/<int:user_id>/', UserDetailsView.as_view(), name='user_details_view'),
    path('broadband_tab/', BroadbandTabView.as_view(), name='broadband_tab'),
    path('populate-table/<str:state>/', populate_table, name='populate_table'),
    path('populate-default-table/<str:region>/', populate_default_table, name='populate_default_table'),
    path('reset_data/', ResetDataView.as_view(), name='reset_data'),
    path('get_combined_table_data/', get_combined_table_data, name='get_combined_table_data'),
    path('get_current_date_time/', get_current_date_time, name='get_current_date_time'),

    path('view_mtd/', views.index, name='view_mtd'),
    path('get_states/', views.get_states, name='get_states'),
    path('get_table_data/', views.get_table_data, name='get_table_data'),

    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),

    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', logout_view, name='logout'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
