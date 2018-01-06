# code by: Francisco Lopez

import tkinter as tk
import os
import pygame

from mutagen import id3
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

listofsongs = []
realnames = []
index = 0
song = 'Song Name'
numRefresh = [0]
LARGE_FONT = ('Helvetica', 9)


def directorychoose():
    directory = filedialog.askdirectory()
    numRefresh[0] = 0
    if directory != '':
        os.chdir(directory)
        numRefresh[0] += 1
        for files in os.listdir(directory):
            if files.endswith(".mp3"):
                realdir = os.path.realpath(files)
                audio = id3.ID3(realdir)
                try:
                    audio = id3.ID3(realdir)
                    realnames.append(audio['TIT2'].text[0])
                except:
                    realnames.append(files)

                pygame.mixer.init()
                pygame.mixer.music.load(realnames[0])
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.1)
    else:
        exit(1)

def updatelist(listbox):
    if numRefresh[0] == 1:
        for items in realnames:
            listbox.insert('end', items)
        numRefresh[0] += 1
        return listbox
    else:
        return listbox

def nextsong():
    global song
    global index
    if index < (len(realnames)-1):
        index += 1
    else:
        index = 0
    song.set(realnames[index])
    pygame.mixer.music.load(realnames[index])
    pygame.mixer.music.play()

def prevsong():
    global song
    global index
    if index > 0:
        index -= 1
    else:
        index = (len(realnames) - 1)
    song.set(realnames[index])
    pygame.mixer.music.load(realnames[index])
    pygame.mixer.music.play()


def stopsong():
    global song
    pygame.mixer.music.stop()
    #v = ""
    # return songname

def play():
    global index
    global song
    pygame.mixer.music.load(realnames[index])
    pygame.mixer.music.play()
    song.set(realnames[index])

def playsong(event):
    global song
    w = event.widget
    cur_index = int(w.curselection()[0])
    global index
    index = cur_index
    song.set(w.get(cur_index))
    pygame.mixer.music.load(w.get(cur_index))
    pygame.mixer.music.play()


def printvalue(event):
    soundvolume = event.widget
    soundvolume = soundvolume.get()
    pygame.mixer.music.set_volume(soundvolume/100)


class SoulSymph(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default='soulicon.ico')
        tk.Tk.wm_title(self, 'Soul Symphony')

        containter = tk.Frame(self)
        containter.pack(side='top', fill='both', expand=True)
        containter.grid_rowconfigure(0, weight=1)
        containter.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(containter)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='Open Folder', command=lambda: directorychoose())
        filemenu.add_command(label='Exit', command=quit)

        menubar.add_cascade(label='File', menu=filemenu)
        menubar.add_command(label='Play', command=lambda: play())
        menubar.add_command(label='Pause', command=lambda: stopsong())
        menubar.add_command(label='Next', command=lambda: nextsong())
        menubar.add_command(label='Previous', command=lambda: prevsong())
        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        global song
        song = StringVar()
        song.set('Select A Folder From The File Menu')

        frame = StartPage(containter, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    songname = NONE

    def __init__(self, parent, controller):
        global songlist
        tk.Frame.__init__(self, parent)

        load = Image.open('vinylart.jpg')
        render = ImageTk.PhotoImage(load)

        img = ttk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=0)

        songname = ttk.Label(self, textvariable=song, font=LARGE_FONT)
        songname.grid(row=1, column=0)

        songlist = tk.Listbox(self, height=10)
        songlist.bind('<<ListboxSelect>>', playsong)

        songlist.grid(row=0, column=1, sticky='nsew')

        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 9))
        listRefresh = ttk.Button(self, text='Refresh List', style='my.TButton', command=lambda: updatelist(songlist))
        listRefresh.grid(row=1, column=1)

        soundlvl = ttk.Scale(self, orient=HORIZONTAL,
                                   length=200,
                                   from_=1, to=100)
        soundlvl.set(10)
        soundlvl.bind('<ButtonRelease-1>', printvalue)

        soundlvl.grid(row=2, column=0)


app = SoulSymph()
app.geometry('360x290')
app.resizable(False, False)
app.mainloop()