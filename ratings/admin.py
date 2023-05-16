from django.contrib import admin

from .models import Rating 

class RatingAdmin(admin.ModelAdmin):
    raw_id_fields = ['trainee']
    list_display = ['content_object', 'trainee', 'value', 'active']
    search_fields = ['trainee__username']
    readonly_fields = ['content_object']

admin.site.register(Rating, RatingAdmin)