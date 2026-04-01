from django.contrib import admin
from .models import Holiday
# Register your models here.
@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'duration_display')
    search_fields = ('name', 'description')
    list_filter = ('start_date', 'end_date')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

    def duration_display(self, obj):
        if obj.is_single_day():
            return "1 day"
        return f"{obj.duration()} days"
    duration_display.short_description = 'Duration'