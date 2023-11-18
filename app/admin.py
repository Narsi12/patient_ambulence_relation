from django.contrib import admin
from .models import USER_Entry,Driver_Entry,Hospital


class DriverEntryAdmin(admin.ModelAdmin):
    list_display = ['name', 'hospital_name', 'vehicle_num', 'phone_num','email'
    ]

admin.site.register(Driver_Entry, DriverEntryAdmin)

class HospitalEntryAdmin(admin.ModelAdmin):
    list_display = ['hospital_name','mobile', 'email', 'location'
    ]
# admin.site.register(Driver_Entry)
admin.site.register(Hospital,HospitalEntryAdmin)
class UserEntryAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone_number'
    ]

admin.site.register(USER_Entry,UserEntryAdmin)
