import unittest
from tkinter import *
from lyric_search import *

class Test_Hasil(unittest.TestCase):

    def setUp(self):
        self.window = Tk()
        self.app = Tampilan(self.window)       
        
    def test_lyric(self):
        self.app.song_result2('hello from the other side')
        self.assertEqual(songs_database[page_counter][0], 'Hello')
        self.assertEqual(artists_database[page_counter][0], 'Adele')

    def test_lyric2(self):
        self.app.song_result2('baby fireworks colors bur')
        self.assertEqual(songs_database[page_counter][0], 'Firework')
        self.assertEqual(artists_database[page_counter][0], 'Katy Perry')

    def tearDown(self):
        self.window.destroy()

if __name__ == "__main__":
    unittest.main()
