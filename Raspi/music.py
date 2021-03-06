import threading
import logging
import os
from pathlib import Path
import simpleaudio as sa
import time
#setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


class MusicState(object):
    def __init__(self):
        musicDir = self.getHomeDir()+ "/music/"
        if not os.path.exists(musicDir):
            logger.error("Music Dir Path does not exist: %s", musicDir)
        self.music_list = self.getMusicPathList(musicDir)
        self.index = 0

    def get_current_song(self):
        playlist_length = len(self.music_list)
        self.index = (self.index)
        return self.music_list[self.index]

    def get_next_song(self):
        playlist_length = len(self.music_list)
        self.index = (self.index+1)%playlist_length
        return self.music_list[self.index]

    def get_previous_song(self):
        playlist_length = len(self.music_list)
        self.index = (self.index-1)%playlist_length
        return self.music_list[self.index]

    def getHomeDir(self):
        homeDir = str(Path.home())
        logger.info("Home Directory found to be : %s",homeDir)
        return homeDir

    def getMusicPathList(self,musicDir):
        list_of_songs = os.listdir(musicDir)
        ouptut = []
        for i in list_of_songs:
            if i.endswith(".wav"):
                p = Path(musicDir+i)
                ouptut.append(p)
        return ouptut



class MusicPlayer(threading.Thread):
    def __init__(self,eventMap):
        threading.Thread.__init__(self)
        self.playEvent = threading.Event()
        logger.debug("Started Music Player Thread")
        self.musicState = MusicState()
        self.play_obj = None
        self.eventMap = eventMap
        self.killThread = threading.Event()
        self.PlayFlag = True

    def next_song(self):
        song_path = self.musicState.get_next_song()
        self.pause()
        self.play_obj = sa.WaveObject.from_wave_file(str(song_path)).play()
        self.PlayFlag = True

    def prev_song(self):
        song_path = self.musicState.get_previous_song()
        self.pause()
        self.play_obj = sa.WaveObject.from_wave_file(str(song_path)).play()
        self.PlayFlag = True

    def pause(self):
        if not self.play_obj == None and self.play_obj.is_playing():
            self.play_obj.stop()
            self.PlayFlag = False
    
    def play(self):
        if not self.play_obj.is_playing():
            song_path = self.musicState.get_current_song()
            self.pause()
            self.play_obj = sa.WaveObject.from_wave_file(str(song_path)).play()
            self.PlayFlag = True
        else:
            logger.info("File is already playing")

    def run(self):
        #Need to do this to instansiate the play_obj
        self.next_song()
        while not self.killThread.is_set():
            for key,value in self.eventMap.items():
                if value.is_set():
                    value.clear()
                    if key =="play":
                        self.play()
                    elif key =="pause":
                            self.pause()
                    elif key == "next":
                        self.next_song()
                    elif key == "previous":
                        self.prev_song()
                    else:
                        logger.warn("Event: %s :in eventmap not recognised",key)
            if self.play_obj.is_playing()==False and self.PlayFlag == True:
                self.next_song()
            time.sleep(0.05)
        logger.info("Kill thread Recieved, thread %s is shutting down", __name__)