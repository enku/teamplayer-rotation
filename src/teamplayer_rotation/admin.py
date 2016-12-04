from django.contrib import admin

from .models import Song


class SongAdmin(admin.ModelAdmin):
    list_display = ('song', 'added')


admin.site.register(Song, SongAdmin)
