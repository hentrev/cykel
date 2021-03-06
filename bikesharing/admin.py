from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from leaflet.admin import LeafletGeoAdmin, LeafletGeoAdminMixin
from preferences.admin import PreferencesAdmin

from .models import Bike
from .models import Rent
from .models import Lock
from .models import Location
from .models import Station
from .models import BikeSharePreferences
from .models import LocationTracker


@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_display = ('bike', 'tracker', 'geo', 'source', 'reported_at')
    list_filter = ('bike', 'tracker', 'source')
    search_fields = ('bike__bike_number', 'tracker__device_id')
    date_hierarchy = 'reported_at'

@admin.register(Bike)
class BikeAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_display = ('bike_number', 'bike_type', 'availability_status',
                    'state', 'last_reported')
    list_filter = ('bike_type', 'availability_status', 'state')
    search_fields = ('bike_number',)
    readonly_fields = ['location']

    @mark_safe
    def location(self, obj):
        if obj is None or obj.current_position() is None:
            return ""
        lat = str(obj.current_position().geo.y)
        lng = str(obj.current_position().geo.x)
        accuracy = ""
        if obj.current_position().accuracy:
            accuracy = ", accuracy: " + str(obj.current_position().accuracy) + "m"
        source = ""
        if (obj.current_position().tracker):
            tracker = obj.current_position().tracker
            source = " (source: <a href='{url}'>tracker {device_id}</a>)".format(
                url=reverse("admin:bikesharing_locationtracker_change", args=(tracker.id,)),
                device_id=tracker.device_id)
        url = "https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=16/{lat}/{lng}".format(lat=lat, lng=lng)
        return "<a href='%s'>%s, %s</a>%s%s" % (url, lat, lng, accuracy, source)
    location.allow_tags = True

@admin.register(Rent)
class RentAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_display = ('bike', 'user', 'rent_start', 'rent_end')
    list_filter = ('rent_start', 'rent_end')
    search_fields = ('bike__bike_number', 'user__username')

@admin.register(LocationTracker)
class LocationTrackerAdmin(LeafletGeoAdmin, admin.ModelAdmin):
    list_display = ('device_id',  'tracker_type', 'bike', 'last_reported', 'battery_voltage')
    list_filter = ('tracker_type', )
    search_fields = ('device_id', 'bike__bike_number')
    readonly_fields = ['location']

    @mark_safe
    def location(self, obj):
        if obj is None or obj.current_position() is None:
            return ""
        lat = str(obj.current_position().geo.y)
        lng = str(obj.current_position().geo.x)
        url = "https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=16/{lat}/{lng}".format(lat=lat, lng=lng)
        return "<a href='%s'>%s, %s</a>" % (url, lat, lng)
    location.allow_tags = True

admin.site.register(Lock, LeafletGeoAdmin)
admin.site.register(Station, LeafletGeoAdmin)
admin.site.register(BikeSharePreferences, PreferencesAdmin)
