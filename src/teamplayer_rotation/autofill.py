import random

from teamplayer.lib.autofill import auto_fill_random

from .models import Song


def rotation_autofill(*, queryset, entries_needed, station):
    """Return songs from the rotation playlist"""
    qs = Song.objects.order_by('?')[:entries_needed]

    songs = [i.song for i in qs]
    entries_needed = entries_needed - len(songs)

    if entries_needed > 0:
        songs = songs + auto_fill_random(
            queryset=queryset,
            entries_needed=entries_needed,
            station=station,
        )

    random.shuffle(songs)

    return songs
