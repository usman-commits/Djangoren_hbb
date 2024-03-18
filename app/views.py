from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import (
    StaffRegistrationForm, 
    DeviceRegistrationForm, 
    ReactivationReport, 
    NccOutLet, 
    DateRangeForm, 
    ProfilePictureForm, 
    UploadPhotoForm, 
    PieDateRangeForm
)
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from .resource import BroadbandResource
from tablib import Dataset
from django.utils.decorators import method_decorator
from django.db.models import Q, Count, Sum
from .models import Broadband, UserProfile
from django.urls import reverse
from datetime import datetime, timedelta
import os
import pandas as pd
import json
from io import BytesIO
import xlsxwriter
import logging
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UploadPhotoForm
from .models import UserProfile
from django.urls import reverse






class StaffRegistrationView(View):
    def get(self, request):
        form = StaffRegistrationForm()
        return render(request, 'staffregistrationform.html', {'form': form})

    def post(self, request):
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Registration successful, now login')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'Invalid data')
        return render(request, 'staffregistrationform.html', {'form': form})







class DeviceRegistrationView(LoginRequiredMixin, View):
    def get(self, request):
        form = DeviceRegistrationForm()
        return render(request, 'home.html', {'form': form})

    def post(self, request):
        form = DeviceRegistrationForm(request.POST)
        if form.is_valid():
            device_registration = form.save(commit=False)
            device_registration.user = request.user  # Set the user field
            device_registration.save()
            messages.success(request, "Submitted successfully")
            # Clear the form after successful submission
            form = DeviceRegistrationForm()
            return HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
            messages.warning(request, "Invalid input data")
        return render(request, 'home.html', {'form': form})


        

class ReactivationReportView(View):
    def get(self, request):
        form = ReactivationReport()
        return render(request, 'reactivationreport.html',locals())
    def post(self, request):
        form = ReactivationReport(request.POST)
        if form.is_valid():
            datetime.now()
            form.save()
            return HttpResponseRedirect(reverse('reactivationreport'))
            messages.success(request, "Submitted successfully")
        else:
            messages.warning(request, "Invalid input data")
        return render(request, 'reactivationreport.html', {'form': form})


class  NccOutLetView(View):
    def get(self, request):
        form =  NccOutLet()
        return render(request, 'nccoutlet.html',locals())
    def post(self, request):
        form =  NccOutLet(request.POST)
        if form.is_valid():
            datetime.now()
            form.save()
            return HttpResponseRedirect('/nccoutlet')
            messages.success(request, "Submitted successful")
        else:
            messages.warning(request, "Invalid input data")
        return render(request, 'nccoutlet.html', {'form': form})



@method_decorator(login_required, name='dispatch')
class ExportDataView(View):
    template_name = 'fetch_data.html'
    def get(self, request):
        ordered_device_types = list(Broadband.objects.values_list('Device_type', flat=True).distinct())
        return render(request, self.template_name, {'ordered_device_types': ordered_device_types})
    def post(self, request):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        device_types_order = request.POST.get('device_types_order')
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        except ValueError:
            return HttpResponse("Invalid date format")
        user_data = Broadband.objects.filter(
            Q(user=request.user),
            Q(Post_date__gte=start_date, Post_date__lt=end_date)
        )
        if device_types_order:
            ordered_device_types = device_types_order.split(',')
            user_data = sorted(user_data, key=lambda x: ordered_device_types.index(x.Device_type) if x.Device_type in ordered_device_types else float('inf'))
       
        resource = BroadbandResource()
        dataset = resource.export(queryset=user_data)
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="EOM Report.xls"'
        return response


class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = ProfilePictureForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.avatar = form.cleaned_data['avatar']
            user_profile.save()
            return HttpResponseRedirect(reverse('profile'))
        return render(request, self.template_name, {'form': form})


class DeleteProfilePictureView(View):
    def post(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        if user_profile.avatar:
            file_path = os.path.join(settings.MEDIA_ROOT, str(user_profile.avatar))
            if os.path.exists(file_path):
                os.remove(file_path)

        user_profile.avatar = None
        user_profile.save()

        return HttpResponseRedirect(reverse('profile'))




class PhotoUploadView(View):
    template_name = 'upload_photo.html'

    def get(self, request):
        form = UploadPhotoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            uploaded_photo = request.FILES.get('uploaded_photo')
            photo_caption = form.cleaned_data.get('photo_caption')  # Assuming 'photo_caption' is the name of the caption field in your form
            new_photo = user_profile.uploaded_photos.create(uploaded_photo=uploaded_photo, photo_caption=photo_caption)
            messages.success(request, "Photo uploaded successfully.")
            return HttpResponseRedirect(reverse('upload_photo'))
        return render(request, self.template_name, {'form': form})






class PhotoView(View):
    template_name = 'view_photo.html'
    def get(self, request):
        user = request.user
        return render(request, self.template_name, {'user': user})

        
def post_or_delete_photo(request):
    user = request.user
    action = request.POST.get('action')

    if action == 'post':
        messages.success(request, "Photo posted successfully.")
    elif action == 'delete':
        user.uploaded_photo = None
        user.save()
        messages.success(request, "Photo deleted successfully.")
    return redirect('view_photo')



# views.py


def dynamic_pie_charts(request):
    # Fetch data from the database
    region_data = (
        Broadband.objects.values('Region').annotate(device_count=Count('id')).order_by('Region')
    )

    device_data = (
        Broadband.objects.values('Device_type').annotate(device_count=Count('id')).order_by('Device_type')
    )

    device_count_data = (
        Broadband.objects.values('Region', 'Device_type').annotate(device_count=Count('Device_type')).order_by('Region', 'Device_type')
    )

    # Prepare data for rendering in the template
    region_labels = [entry['Region'] for entry in region_data]
    region_sizes = [entry['device_count'] for entry in region_data]

    device_labels = [entry['Device_type'] for entry in device_data]
    device_sizes = [entry['device_count'] for entry in device_data]

    # Device count data for one specific region (e.g., 'North East')
    one_region_device_count_data = [
        {'Region': entry['Region'], 'Device_type': entry['Device_type'], 'device_count': entry['device_count']}
        for entry in device_count_data if entry['Region'] == 'North East'
    ]

    one_region_device_count_labels = [entry['Device_type'] for entry in one_region_device_count_data]
    one_region_device_count_sizes = [entry['device_count'] for entry in one_region_device_count_data]

    # Device count data for North West region
    north_west_region_device_count_data = [
        {'Region': entry['Region'], 'Device_type': entry['Device_type'], 'device_count': entry['device_count']}
        for entry in device_count_data if entry['Region'] == 'North West'
    ]

    north_west_region_device_count_labels = [entry['Device_type'] for entry in north_west_region_device_count_data]
    north_west_region_device_count_sizes = [entry['device_count'] for entry in north_west_region_device_count_data]

    # Device count data for South East region
    south_east_region_device_count_data = [
        {'Region': entry['Region'], 'Device_type': entry['Device_type'], 'device_count': entry['device_count']}
        for entry in device_count_data if entry['Region'] == 'South East'
    ]

    south_east_region_device_count_labels = [entry['Device_type'] for entry in south_east_region_device_count_data]
    south_east_region_device_count_sizes = [entry['device_count'] for entry in south_east_region_device_count_data]

    # Device count data for South South region
    south_south_region_device_count_data = [
        {'Region': entry['Region'], 'Device_type': entry['Device_type'], 'device_count': entry['device_count']}
        for entry in device_count_data if entry['Region'] == 'South South'
    ]

    south_south_region_device_count_labels = [entry['Device_type'] for entry in south_south_region_device_count_data]
    south_south_region_device_count_sizes = [entry['device_count'] for entry in south_south_region_device_count_data]

    # Device count data for Lagos region
    lagos_region_device_count_data = [
        {'Region': entry['Region'], 'Device_type': entry['Device_type'], 'device_count': entry['device_count']}
        for entry in device_count_data if entry['Region'] == 'Lagos'
    ]

    lagos_region_device_count_labels = [entry['Device_type'] for entry in lagos_region_device_count_data]
    lagos_region_device_count_sizes = [entry['device_count'] for entry in lagos_region_device_count_data]

    # Device count data for West region
    west_region_device_count_data = [
        {'Region': entry['Region'], 'Device_type': entry['Device_type'], 'device_count': entry['device_count']}
        for entry in device_count_data if entry['Region'] == 'West'
    ]

    west_region_device_count_labels = [entry['Device_type'] for entry in west_region_device_count_data]
    west_region_device_count_sizes = [entry['device_count'] for entry in west_region_device_count_data]

    # Convert data to JSON strings
    region_labels_json = json.dumps(region_labels)
    region_sizes_json = json.dumps(region_sizes)
    device_labels_json = json.dumps(device_labels)
    device_sizes_json = json.dumps(device_sizes)
    one_region_device_count_labels_json = json.dumps(one_region_device_count_labels)
    one_region_device_count_sizes_json = json.dumps(one_region_device_count_sizes)
    north_west_region_device_count_labels_json = json.dumps(north_west_region_device_count_labels)
    north_west_region_device_count_sizes_json = json.dumps(north_west_region_device_count_sizes)
    south_east_region_device_count_labels_json = json.dumps(south_east_region_device_count_labels)
    south_east_region_device_count_sizes_json = json.dumps(south_east_region_device_count_sizes)
    south_south_region_device_count_labels_json = json.dumps(south_south_region_device_count_labels)
    south_south_region_device_count_sizes_json = json.dumps(south_south_region_device_count_sizes)
    
    lagos_region_device_count_labels_json = json.dumps(lagos_region_device_count_labels)
    lagos_region_device_count_sizes_json = json.dumps(lagos_region_device_count_sizes)
    west_region_device_count_labels_json = json.dumps(west_region_device_count_labels)
    west_region_device_count_sizes_json = json.dumps(west_region_device_count_sizes)

    context = {
        'region_labels_json': region_labels_json,
        'region_sizes_json': region_sizes_json,
        'device_labels_json': device_labels_json,
        'device_sizes_json': device_sizes_json,
        'one_region_device_count_labels_json': one_region_device_count_labels_json,
        'one_region_device_count_sizes_json': one_region_device_count_sizes_json,
        'north_west_region_device_count_labels_json': north_west_region_device_count_labels_json,
        'north_west_region_device_count_sizes_json': north_west_region_device_count_sizes_json,
        'south_east_region_device_count_labels_json': south_east_region_device_count_labels_json,
        'south_east_region_device_count_sizes_json': south_east_region_device_count_sizes_json,
        'south_south_region_device_count_labels_json': south_south_region_device_count_labels_json,
        'south_south_region_device_count_sizes_json': south_south_region_device_count_sizes_json,
        'lagos_region_device_count_labels_json': lagos_region_device_count_labels_json,
        'lagos_region_device_count_sizes_json': lagos_region_device_count_sizes_json,
        'west_region_device_count_labels_json': west_region_device_count_labels_json,
        'west_region_device_count_sizes_json': west_region_device_count_sizes_json,
    }

    return render(request, 'pie_chart.html', context)

    



def export_pie_data(request):
    if request.method == 'POST':
        form = PieDateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Filter data based on the selected date range
            data = Broadband.objects.filter(Post_date__range=[start_date, end_date])

            # Extract relevant columns for pie chart data
            pie_data = data.values('Region', 'Device_type').annotate(device_count=Count('Device_type')).order_by('Region', 'Device_type')
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(pie_data)

            # Create an Excel writer using XlsxWriter
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)

            output.seek(0)

            # Set up response for file download
            response = HttpResponse(output.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename=pie_data_export.xlsx'

            # Display a success message
            messages.success(request, 'Pie chart data exported successfully.')
            return response

    else:
        form = PieDateRangeForm()

    return render(request, 'export_pie_data.html', {'form': form})





class RegionView(View):
    template_name = 'region_view.html'

    def get(self, request, region):
        states = Broadband.STATE_CHOICES.get(Region, [])
        return render(request, self.template_name, {'Region': Region, 'States': States})

class StateView(View):
    template_name = 'state_view.html'

    def get(self, request, state):
        state_data = Broadband.objects.filter(State=state)
        return render(request, self.template_name, {'State': State, 'state_data': state_data})

class UserDetailsView(View):
    template_name = 'user_details_view.html'

    def get(self, request, user_id):
        user = Broadband.objects.get(id=user_id)
        
        # Calculate the total number of devices for each type
        mifi_count = user.MIFI
        router_count = user.Router
        odu_count = user.ODU
        d5g_router_count = user.d5G_Router
        
        # Calculate the total count of each device type
        total_devices = mifi_count + router_count + odu_count + d5g_router_count
        
        # Add your logic to calculate total, target, achieved, LMTD, and growth here
        user_details = {
            'name': user.HSE_name,  # Assuming HSE_name is the user's name
            'state': user.State,
            'mifi': mifi_count,
            'router': router_count,
            'ODU': odu_count,
            '5g_router': d5g_router_count,
            'total': total_devices,
            'target': 50,  # Replace with your logic
            'achieved': 0,  # Replace with your logic
            'LMTD': 0,  # Replace with your logic
            'growth': 0,  # Replace with your logic
        }
        return render(request, self.template_name, {'user_details': user_details})

class BroadbandTabView(View):
    template_name = 'broadband_tab.html'

    def get(self, request):
        return render(request, self.template_name, {'Broadband': Broadband})

def populate_table(request, state):
    # Fetch data for the selected state
    state_data = Broadband.objects.filter(State=state)

    # Check if data is available
    if state_data:
        data_list = []
        for entry in state_data:
            data_list.append({
                'sn': len(data_list) + 1,
                'hse_name': entry.name,
                'State': entry.state,
                'mifi': entry.MIFI,
                'router': entry.Router,
                'odu': entry.ODU,
                'd5g_router': entry.d5G_Router,
                'total': entry.total_devices,
                'target': 50,  # Replace with the actual target value
                'achieved_percentage': entry.total_percentage_achieved,
                'lmtd': entry.achieved_previous_month,
                'growth_percentage': entry.growth_percentage,
            })
        return JsonResponse(data_list, safe=False)
    else:
        return JsonResponse([], safe=False)


def populate_default_table(request, region):
    # Fetch data for the selected region
    default_state_data = Broadband.objects.filter(Region=region).first()

    # Check if data is available
    if default_state_data:
        data = {
            'sn': 1,
            'hse_name': default_state_data.name,
            'State': default_state_data.state,
            'mifi': default_state_data.MIFI,
            'router': default_state_data.Router,
            'odu': default_state_data.ODU,
            'd5g_router': default_state_data.d5G_Router,
            'total': default_state_data.total_devices,
            'target': 50,  # Replace with the actual target value
            'achieved_percentage': default_state_data.total_percentage_achieved,
            'lmtd': default_state_data.achieved_previous_month,
            'growth_percentage': default_state_data.growth_percentage,
        }
        return JsonResponse([data], safe=False)
    else:
        return JsonResponse([], safe=False)


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))




@require_GET
def populate_default_table(request, region):
    # Fetch data from the model based on the region
    data = Broadband.objects.filter(Region=region)
    
    # Serialize the data into JSON format
    serialized_data = [{
        'name': entry.Customer_name,
        'state': entry.State,
        'MIFI': entry.MIFI,
        'Router': entry.Router,
        'ODU': entry.ODU,
        'd5G_Router': entry.d5G_Router,
        'total_devices': entry.total_devices,
        'total_percentage_achieved': entry.total_percentage_achieved,
        'achieved_previous_month': entry.achieved_previous_month,
        'growth_percentage': entry.growth_percentage
    } for entry in data]
    
    # Return the serialized data as JSON response
    return JsonResponse(serialized_data, safe=False)

@require_GET
def populate_table(request, state):
    # Fetch data from the model based on the state
    data = Broadband.objects.filter(State=state)
    
    # Serialize the data into JSON format
    serialized_data = [{
        'name': entry.Customer_name,
        'state': entry.State,
        'MIFI': entry.MIFI,
        'Router': entry.Router,
        'ODU': entry.ODU,
        'd5G_Router': entry.d5G_Router,
        'total_devices': entry.total_devices,
        'total_percentage_achieved': entry.total_percentage_achieved,
        'achieved_previous_month': entry.achieved_previous_month,
        'growth_percentage': entry.growth_percentage
    } for entry in data]
    
    # Return the serialized data as JSON response
    return JsonResponse(serialized_data, safe=False)




def index(request):
    return render(request, 'view_mtd.html')



def get_states(request):
    region = request.GET.get('region')
    states = Broadband.STATE_CHOICES.get(region, [])
    return JsonResponse({'states': states})



def get_table_data(request):
    state = request.GET.get('state')
    month = request.GET.get('month')  # Assuming month is passed as a numeric value (e.g., 1 for January)
    year = request.GET.get('year')

    # Filter broadband data by state, month, and year
    broadband_data = Broadband.objects.filter(State=state, Post_date__month=month, Post_date__year=year)

    # Calculate the sum totals for each device type for each user
    table_data = []
    for user in broadband_data.values_list('HSE_name', flat=True).distinct():
        user_data = {
            'HSE_name': user,
            'State': state,
            'MIFI': broadband_data.filter(HSE_name=user, Device_type='MIFI').count(),
            'Router': broadband_data.filter(HSE_name=user, Device_type='Router').count(),
            'ODU': broadband_data.filter(HSE_name=user, Device_type='ODU').count(),
            'd5G_Router': broadband_data.filter(HSE_name=user, Device_type='5G Router').count(),
            'total': broadband_data.filter(HSE_name=user).count(),
            'lmtd': '',  # Placeholder for last month to date data, modify as per your requirement
            'growth': ''  # Placeholder for growth data, modify as per your requirement
        }
        table_data.append(user_data)
    lmtd_start_date = datetime(int(year), int(month), 1) - timedelta(days=1)
    lmtd_end_date = lmtd_start_date.replace(day=1)
    lmtd_total_devices = Broadband.objects.filter(State=state, Post_date__gte=lmtd_start_date, Post_date__lt=lmtd_end_date).aggregate(total_devices=Count('Device_type'))['total_devices']
    corresponding_date = datetime.now().replace(month=int(month), year=int(year)).strftime('%B %d, %Y')
    return JsonResponse({'table_data': table_data, 'corresponding_date': corresponding_date, 'lmtd_total_devices': lmtd_total_devices})



def get_combined_table_data(request):
    region = request.GET.get('region')
    combined_table_data = Broadband.objects.filter(State__region=region).values(
        'HSE_name', 'State', 'MIFI', 'Router', 'ODU', 'd5G_Router', 'total', 'LMTD', 'growth'
    )
    data = list(combined_table_data)
    return JsonResponse({'combined_table_data': data})



class ResetDataView(View):
    def get(self, request):
        current_date = timezone.now()
        if current_date.day == 1:
            Broadband.objects.all().update(
                MIFI=0,
                Router=0,
                ODU=0,
                d5G_Router=0,
                achieved_previous_month=0.0
            )
            return JsonResponse({'message': 'Data reset successfully for the new month.'})
        else:
            return JsonResponse({'message': 'It is not the beginning of a new month.'})



def get_current_date_time(request):
    current_date_time = datetime.now().strftime('%d %B %Y, %H:%M:%S')
    return JsonResponse({'current_date_time': current_date_time})


def generate_region_data(request):
    region = request.GET.get('region')
    region_data = fetch_data_for_region(region)
    return JsonResponse({'region_data': region_data})


def get_all_states_table_data(request):
    if request.method == 'GET':
        region = request.GET.get('region')  
        if region:
            broadband_data = Broadband.objects.filter(Region=region)
            data = {
                'table_data': list(broadband_data.values()),  
                'corresponding_date': datetime.now().strftime("%d/%b/%Y"), 
            }
            return JsonResponse(data)  
        else:
            return JsonResponse({'error': 'Region parameter is missing'}) 
    else:
        return JsonResponse({'error': 'Invalid request method'}) 










        





        
