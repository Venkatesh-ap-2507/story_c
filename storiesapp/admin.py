from django.contrib import admin
from .models import User, Story


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username','password')

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'contributions', 'created_by','image')
    search_fields = ('title',)

admin.site.register(User, UserAdmin)

admin.site.register(Story, StoryAdmin)