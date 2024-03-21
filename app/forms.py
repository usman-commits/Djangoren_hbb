from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Broadband, ReactivationReport, NccOutLet, UserProfile, UploadPhoto





class LoginForm(AuthenticationForm):
     username = UsernameField(widget=forms.TextInput(attrs={'autofocus ':'True', 'class':'form-control'}))
     password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class StaffRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password', 'class':'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


    
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label=' Confirm New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


    

class DeviceRegistrationForm(forms.ModelForm):
    class Meta:
        model = Broadband
        fields = ['HSE_name', 'Region', 'State', 'Device_type', 'MSISDN', 'IMEI', 'Alternate', 'Customer_name']
        widgets = {
            'HSE_name': forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'Region': forms.Select(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'State': forms.Select(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'Device_type': forms.Select(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'MSISDN': forms.NumberInput(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'IMEI': forms.NumberInput(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'Alternate': forms.NumberInput(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'Customer_name': forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}),
            
        }
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the 'user' field exists in the form
        if 'user' in self.fields:
            # Set 'user' field as not required
            self.fields['user'].required = False

    def clean(self):
        cleaned_data = super().clean()
        msisdn = cleaned_data.get('MSISDN')
        imei = cleaned_data.get('IMEI')

        existing_msisdn_record = Broadband.objects.filter(MSISDN=msisdn).first()
        existing_imei_record = Broadband.objects.filter(IMEI=imei).first()

        if existing_msisdn_record:
            existing_msisdn_date = existing_msisdn_record.Post_date.strftime('%Y-%m-%d %H:%M:%S')
            self.add_error('MSISDN', f'A record with this MSISDN already exists (submitted on {existing_msisdn_date}).')

        if existing_imei_record:
            existing_imei_date = existing_imei_record.Post_date.strftime('%Y-%m-%d %H:%M:%S')
            self.add_error('IMEI', f'A record with this IMEI already exists (submitted on {existing_imei_date}).')

        return cleaned_data






class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class UploadPhotoForm(forms.ModelForm):
    photo_caption = forms.CharField(max_length=100, required=False)
    class Meta:
        model = UploadPhoto
        fields = ['Region','State','uploaded_photo', 'photo_caption']
        widgets = {
            'Region': forms.Select(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'State': forms.Select(attrs={'autofocus': 'True', 'class': 'form-control'}),
       }



class ReactivationReport(forms.ModelForm):
    class Meta:
        model = ReactivationReport
        fields = ['HSE_name','Region','State','Total_calls','Successful_calls','Unsuccessful_calls','Successful_bundle']
        widgets = {
            'HSE_name': forms.TextInput(attrs={'class':'form-control'}),
            'Region': forms.Select(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'State': forms.Select(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'Total_calls': forms.NumberInput(attrs={'autofocus':'True','class':'form-control'}),
            'Successful_calls': forms.NumberInput(attrs={'autofocus':'True','class':'form-control'}),
            'Unsuccessful_calls': forms.NumberInput(attrs={'autofocus':'True','class':'form-control'}),
            'Successful_bundle': forms.NumberInput(attrs={'autofocus':'True','class':'form-control'}),
        }
    

class NccOutLet(forms.ModelForm):
    class Meta:
        model = NccOutLet
        fields = ['HSE_name','Region','State','Total_certified_outlet','Outlet_visited', 'Outlet_with_device', 'Total_devices_in_outlet','Total_devices_sold']
        widgets = {
            'HSE_name': forms.TextInput(attrs={'class':'form-control'}),
            'Region': forms.Select(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'State': forms.Select(attrs={'autofocus': 'True', 'class': 'form-control'}),
            'Total_certified_outlet': forms.NumberInput(attrs={'autofocus':'True','class':'form-control'}),
            'Outlet_visited': forms.NumberInput(attrs={'autofocus':'True','class':'form-control'}),
            'Outlet_with_device': forms.NumberInput(attrs={'autofocus':'True','class':'form-control'}),
            'Total_devices_in_outlet': forms.NumberInput(attrs={'autofocus':'True','class':'form-control'}),
            'Total_devices_sold': forms.NumberInput(attrs={'autofocus':'True','class':'form-control'}),
            
        }

class DateRangeForm(forms.Form):
    start_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type':'date'}))


# forms.py



class PieDateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
