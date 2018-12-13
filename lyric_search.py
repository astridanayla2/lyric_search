
# Astrida Nayla Fauzia
# 1806235826

# mengimpor selenium.webdriver.chrome.options untuk memungkinkan headless mode
# mengimpor library beautifulsoup sebagai web scrapping untuk mempermudah mengambil informasi dari web
# mengimpor modul-modul tkinter secara keseluruhan
# mengimpor library selenium untuk method webdrive google chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import *
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import time
import os

"""Program ini mengambil input dari user berupa lirik lagu, lalu mengembalikan judul, nama penyanyi, dan cover
album dari lirik lagu yang dicari. Program ini juga akan memunculkan browser yang membuka lagu tersebut di Youtube"""

# kelas utama yang menginherit dari superclass Frame
class Tampilan(Frame):
    def __init__(self, master):
        # menginherit instances dari superclass Frame
        super().__init__(master)
        
        # judul window
        master.title("Lyric Search [by Astrida Nayla]")

        # membuat label masukan lirik
        self.label = Label(self, text= "Enter a lyric:", font="Arial 16 bold")
        self.label.grid(row=1, column=2)

        # membuat entry untuk input lirik
        self.entry = Entry(self, font="Arial 16")
        self.entry.bind("<Return>", lambda _:self.gui())
        self.entry.grid(row=2, column=2)

        # membuat canvas untuk hasil pencarian
        self.canvas = Canvas(self, width=350, height=250, bg="white")
        self.canvas.grid(row=3, column=2)

    def gui(self):
        lyric_input = str(self.entry.get())
        if lyric_input.isdecimal() == True:
            print("Please enter a valid lyric")
            return
        elif len(lyric_input.split()) <= 1:
            print("please enter a complete lyric")
            return

        # mengambil input lirik untuk dicari judul lagunya 
        # membuat button next dan previous untuk hasil-hasil lagu
        next_button = Button(self, text="Next", command=self.next_song)
        next_button.grid(row=4, column=2)
        prev_button = Button(self, text="Previous", command=self.prev_song)
        prev_button.grid(row=5, column=2)

        # membuat button untuk play song hasil search lagu
        play_button = Button(self, text="Play Song", command=self.play_song)
        play_button.grid(row=6, column=2)
        
        # menghapus isi canvas jika ada input lirik baru
        self.canvas.delete("all")

        self.song_result(lyric_input)

        # menambahkan icon musik
        music_icon = PhotoImage(file="Eighth-Note-Double.png")
        self.canvas.create_image(175, 100, image=music_icon)
                    
        # memunculkan judul lagu, artist, dan cover album di canvas
        self.canvas.create_text(175, 20, text= "Search result:", font="Arial 16 bold", fill="purple")
        self.canvas.create_text(175, 50, text= str(songs_database[page_counter][0]).upper(), font="Arial 16 bold")
        self.canvas.create_text(175, 75, text= str(artists_database[page_counter][0]), font="Arial 16 bold")

    def song_result(self, lyric_input):
        # membuka wedriver untuk mengakses google chrome, diatur jadi headless mode supaya tidak tampak
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")

        chrome_path = "/Users/dexter-dee/Desktop/lyric_search/chromedriver"
        self.driver = webdriver.Chrome(options=self.chrome_options, executable_path=chrome_path)

        # membuka situs genius.com dan mencari lirik untuk menentukan judul lagu
        link_genius = "https://genius.com/search?q={}".format(lyric_input)
        self.driver.get(link_genius)
        time.sleep(3)

        # mengambil tiap kemungkinan judul dan artist dari lagu yang dicari
        page_source = self.driver.page_source
        page_source = BeautifulSoup(page_source, "lxml")
        track = page_source.find_all("div", {"class":"mini_card-title"})
        time.sleep(3)
        artists = page_source.find_all("div", {"class":"mini_card-subtitle"})
        time.sleep(3)

        # list berisi string judul lagu-lagu hasil pencarian
        song_titles = [song.string for song in track]
        self.title = song_titles[0]
        # list berisi page source untuk nama-nama artist hasil pencarian
        song_artists = [str(artist) for artist in artists]
        
        # slicing nama artist dari page source
        artist = []
        for element in song_artists:
            string = element.split("\n")
            artist.append(string[1][8:-8])

        # menambah daftar artist ke dictionary, dengan urutan/page number sebagai key
        count = 1
        for people in artist:
            artists_database[count] = [people]
            count += 1

        # menambah daftar judul lagu ke dictionary, dengan urutan/page number sebagai key
        counter = 1
        for track in song_titles:
            if counter != count:
                songs_database[counter] = [track]
                counter += 1

        # menutup driver setelah program selesai
        self.driver.quit()
        
           
    def play_song(self):
        # mencari video lagu yang dicari di youtube dengan mode headless agar tidak tampak
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")

        chrome_path2 = "/Users/dexter-dee/Desktop/lyric_search/chromedriver"
        driver2 = webdriver.Chrome(options=self.chrome_options, executable_path=chrome_path2)

        youtube_search = str(songs_database[page_counter][0]) + " " + str(artists_database[page_counter][0])
        link_youtube = "https://www.youtube.com/results?search_query={}".format(youtube_search)
        driver2.get(link_youtube)
        time.sleep(3)

        page_source = driver2.page_source
        page_source = BeautifulSoup(page_source, "lxml")
        video_path = page_source.find_all("a", {"class":"yt-simple-endpoint inline-block style-scope ytd-thumbnail"})
        time.sleep(3)

        # menutup driver setelah program selesai
        driver2.quit()

        # list berisi page source link video lagu-lagu hasil pencarian
        video_link = [str(link) for link in video_path]
        
        # slicing link dari page source
        link = []
        for element in video_link:
            string = element.split()
            link.append(string[6][6:-1])

        # menambah daftar link video ke dictionary, dengan urutan/page number sebagai key
        count = 1
        for element in link:
            link_database[count] = [element]
            count += 1
        
        # membuka lagi driver yang kali ini tidak headless, untuk menunjukkan video lagu di youtube
        chrome_path3 = "/Users/dexter-dee/Desktop/chromedriver"
        driver3 = webdriver.Chrome(executable_path=chrome_path3)
        driver3.get("https://www.youtube.com{}".format(str(link_database[page_counter][0])))
        
    def next_song(self):
        # memanggil kembali variabel page_counter, karena kalau tidak fungsi ini akan error
        global page_counter
        # kalau hasil sudah paling terakhir, next button tidak akan bekerja
        if page_counter == len(songs_database):
            pass
        else:
            # memunculkan hasil pencarian lagu selanjutnya
            page_counter += 1
            self.gui()

    def prev_song(self):
        # memanggil kembali variabel page_counter, karena kalau tidak fungsi ini akan error
        global page_counter
        # kalau hasil sudah paling awal, prev button tidak akan bekerja
        if page_counter == 1:
            pass
        else:
            # memunculkan hasil pencarian lagu sebelumnya
            page_counter -= 1
            self.gui()

# database untuk penyimpanan hasil pencarian
songs_database = {}
artists_database = {}
album_image_database = {}
link_database = {}

page_counter = 1

# fungsi main untuk menjalankan program secara keseluruhan    
def main():
    window = Tk()
    app = Tampilan(window)
    # karena frame, di pack agar muncul
    app.pack()
    window.mainloop()
    
if __name__ == "__main__":
    main()

# FUCKING TO DO LIST
# ngambil image album dr genius, taruh di canvas
# ngebetulin error handling dari input
# Image.open()


