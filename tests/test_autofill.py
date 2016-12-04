from unittest.mock import patch

from django.test import TestCase
from teamplayer.models import LibraryItem, Player, Station

from teamplayer_rotation.autofill import rotation_autofill
from teamplayer_rotation.models import Song


class RotationAutofillTest(TestCase):
    """tests for the rotation_autofill function"""
    def setUp(self):
        parent = super()
        parent.setUp()

        self.dj_ango = Player.dj_ango()

        artists = (
            'Britney Spears',
            'KMFDM',
            'Kanye West',
            'Katie Melua',
            'Marilyn Manson',
            'Nine Inch Nails',
            'Norah Jones',
            'Sufjan Stevens',
            'The Glitch Mob',
            'edIT',
        )
        # let's fill the library with some songage
        for artist in artists:
            filename = '{0}.mp3'.format(artist.lower().replace(' ', '_'))
            songfile = LibraryItem(
                filename=filename,
                artist=artist,
                title='Silent Night',
                album='Various Artists Do Silent Night',
                genre='Unknown',
                length=300,
                filesize=3000,
                station_id=1,
                mimetype='audio/mp3',
                added_by=self.dj_ango,
            )
            songfile.save()

    def test_empty_playlist_returns_random_songs(self):
        # given the empty rotation playlist
        assert Song.objects.count() == 0

        # when we call rotation_autofill()
        queryset = LibraryItem.objects.all()
        station = Station.main_station()
        result = rotation_autofill(
            queryset=queryset,
            entries_needed=3,
            station=station,
        )

        # then we get the number of requested songs
        self.assertEqual(len(result), 3)

        # and they are a subset of the queryset
        queryset = set(queryset)
        result = set(result)
        self.assertTrue(result.issubset(queryset))

    def test_only_songs_from_playlist_when_enough_entries(self):
        # given the songs in the playlist
        songs = LibraryItem.objects.all()
        song1 = songs[1]
        song2 = songs[3]
        song3 = songs[5]
        song4 = songs[7]

        with patch('teamplayer_rotation.models.IPCHandler.send_message'):
            Song.objects.create(song=song1)
            Song.objects.create(song=song2)
            Song.objects.create(song=song3)
            Song.objects.create(song=song4)

        # when we call rotation_autofill()
        queryset = LibraryItem.objects.all()
        station = Station.main_station()
        result = rotation_autofill(
            queryset=queryset,
            entries_needed=3,
            station=station,
        )

        # then we get the number of requested songs
        self.assertEqual(len(result), 3)

        # and they are songs from our playlist
        for song in result:
            self.assertTrue(song in {song1, song2, song3, song4})

    def test_random_songs_added_when_not_enough_entries(self):
        # given the songs in the playlist
        songs = LibraryItem.objects.all()
        song1 = songs[1]
        song2 = songs[3]
        song3 = songs[5]

        with patch('teamplayer_rotation.models.IPCHandler.send_message'):
            Song.objects.create(song=song1)
            Song.objects.create(song=song2)
            Song.objects.create(song=song3)

        # when we call rotation_autofill() wanting more songs than are in
        # our playlist
        queryset = LibraryItem.objects.all()
        station = Station.main_station()
        result = rotation_autofill(
            queryset=queryset,
            entries_needed=4,
            station=station,
        )

        # then we get the number of requested songs
        self.assertEqual(len(result), 4)

        # with all our playlist songs plus the 1
        result = set(result)
        playlist = {song1, song2, song3}
        self.assertEqual(result.intersection(playlist), playlist)
