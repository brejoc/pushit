from django.contrib import admin
from timeline.models import Event
from timeline.models import Activity

class EventAdmin(admin.ModelAdmin):
    pass

class ActivityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)
admin.site.register(Activity, ActivityAdmin)
