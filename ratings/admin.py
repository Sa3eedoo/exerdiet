from django.contrib import admin

from .models import Rating 

class RatingAdmin(admin.ModelAdmin):
    raw_id_fields = ['trainee']
    list_display = ['content_object', 'trainee', 'value', 'active', 'content_type']
    search_fields = ['trainee__user__username']
    readonly_fields = ['content_object']
    list_filter = ['active', 'value']

admin.site.register(Rating, RatingAdmin)