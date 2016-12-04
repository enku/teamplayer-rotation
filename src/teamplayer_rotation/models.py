from django.db import models
from teamplayer.lib.websocket import IPCHandler
from teamplayer.models import LibraryItem


class Song(models.Model):
    """The LibraryItems to use in our playlist"""
    song = models.OneToOneField(LibraryItem)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.song)

    def save(self, *args, **kwargs):
        parent = super(Song, self)
        return_value = parent.save(*args, **kwargs)

        IPCHandler.send_message('queue_status', {})

        return return_value
