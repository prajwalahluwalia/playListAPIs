import json
import pandas as pd
import math
from lyricsfandom import LyricWiki

class PlayList:
    def __init__(self):
        self.df = pd.DataFrame()
        self.filepath = 'playlist.json'
        self.normalized = ['id','title','danceability','energy','mode','acousticness','tempo','duration_ms','num_sections','num_segments', 'rating']

    #generic functions
    def get_data(self):
        try: 
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                
            self.df = pd.DataFrame(data)
            
            for cols in self.normalized:
                if cols not in self.df.columns:
                    self.df[cols] = 'NA'
                    
            return self.df
        
        except Exception as e:
            return(e)

    def get_song_by_id(self, song_id):
        vals = {}
        
        if not len(self.df):
            self.df = self.get_data()
        try:
            for index, row in self.df.iterrows():
                if int(index)==int(song_id-1):
                    vals['index']=int(index)
                    for i in self.normalized:
                        if i in row and row[i]:
                            vals[i] = row[i]
                        else:
                            vals[i] = 'NA'
            return vals
        
        except Exception as e:
            return(e)

    def get_all_title(self):
        allSongs = []
        if not len(self.df):
            self.df = self.get_data()
            
        try:
            for index,rows in self.df.iterrows():
                allSongs.append([rows['title'], rows['rating']])
                
            return allSongs
        
        except Exception as e:
            return(e)
            
    def update_rating(self, song_id, rating):
        if not len(self.df):
            self.df = self.get_data()
            
        try:
            for index, row in self.df.iterrows():
                if int(index)==int(song_id-1):
                    self.df.loc[index, 'rating'] = rating

            return
        
        except Exception as e:
            return e

    def get_song_lyrics(self, song_name):
        if not len(self.df):
            self.df = self.get_data()
        wiki = LyricWiki()
        try:
            song = wiki.search_song(song_name=song_name, artist_name='')
            if song:
                lyrics = song.get_lyrics()
            
                return lyrics
            else:
                return False
        except Exception as e:
            return e
