from django.contrib import admin
from .models import Video

class HomeAdmin(admin.ModelAdmin):
    list_display = ('category','video','description', 'title')
    list_filter = ('created','title','category')
    search_fields = ('title', 'category', 'created', 'description')
    ordering = ['created',]

admin.site.register(Video, HomeAdmin)
