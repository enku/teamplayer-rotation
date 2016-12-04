"""tests for the teamplayer_rotation models"""
from unittest.mock import patch

from django.test import TestCase
from teamplayer.models import LibraryItem, Player

from teamplayer_rotation.models import Song


class SongTest(TestCase):
    """tests for the Song model"""
    def setUp(self):
        dj_ango = Player.dj_ango()
        self.library_item = LibraryItem(
            filename='Bing Crosby - Silent Night.mp3',
            artist='Bing Crosby',
            title='Silent Night',
            album='Various Artists Do Silent Night',
            genre='Unknown',
            length=300,
            filesize=3000,
            station_id=1,
            mimetype='audio/mp3',
            added_by=dj_ango,
        )

        self.library_item.save()

    def test_str(self):
        # given the song in rotation
        song = Song(song=self.library_item)

        # when we call it's str() method
        result = str(song)

        # then we get the library's song string()
        self.assertEqual(result, str(song.song))

    def test_save_sends_ipc_message(self):

        # given the song in rotation
        song = Song(song=self.library_item)

        # when we call its .save() method
        path = 'teamplayer_rotation.models.IPCHandler.send_message'
        with patch(path) as send_message:
            song.save()

        # then an IPC message is sent
        send_message.assert_called_with('queue_status', {})
