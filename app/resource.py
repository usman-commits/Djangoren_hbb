from import_export import resources , fields, widgets
from .models import Broadband, ReactivationReport, NccOutLet
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from django.http import HttpResponse 




class BroadbandResource(resources.ModelResource):
    class Meta:
        model = Broadband
        fields = ('HSE_name', 'Region', 'State', 'Device_type', 'MSISDN', 'IMEI', 'Alternate', 'Customer_name', 'Post_date')
        export_order = ('Region', 'State', 'HSE_name', 'Device_type', 'IMEI', 'MSISDN', 'Alternate','Customer_name', 'Post_date')

    def dehydrate_IMEI(self, broadband):
        return "'" + str(broadband.IMEI) if broadband.IMEI else ''
    
        

class ReactivationReportResource(resources.ModelResource):
    class Meta:
        model = ReactivationReport
        fields = ('HSE_name','Total_calls','Successful_calls','Unsuccessful_calls','Successful_bundle')
        export_order = ('HSE_name','Total_calls','Successful_calls','Unsuccessful_calls','Successful_bundle')

  


class NccOutLetResource(resources.ModelResource):
    class Meta:
        model = NccOutLet
        fields = (' HSE_name','Total_certified_outlet','Outlet_visited',' Outlet_with_device ',' Total_devices_in_outlet',' Total_devices_sold')
        export_order = (' HSE_name','Total_certified_outlet','Outlet_visited','Outlet_with_device ','Total_devices_in_outlet','Total_devices_sold')




      