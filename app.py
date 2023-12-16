from flask import Flask, request, render_template, redirect, url_for
import requests
import json
import pandas as pd
import math
import threading
from lyricsfandom import LyricWiki

#Initial declarations
wiki = LyricWiki()
df = pd.DataFrame()
filePath = 'playlist.json'

#initializing flask app
app = Flask(__name__)

#normalized list as per requirement
normalized = ['id','title','danceability','energy','mode','acousticness','tempo','duration_ms','num_sections','num_segments', 'rating']

#generic functions
def get_data(filePath):
    try: 
        with open(filePath, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df['rating']=4
        return df
    except Exception as e:
        return(e)

def get_song_by_id(df, song_id):
    vals = {}
    try:
        for index, row in df.iterrows():
            if int(index)==int(song_id-1):
                vals['index']=int(index)
                for i in normalized:
                    vals[i] = row[i]
        return vals
    
    except Exception as e:
        return(e)

def get_all_title(df):
    allSongs = []
    try:
        for index,rows in df.iterrows():
            allSongs.append([rows['title'], rows['rating']])
            
        return allSongs
    
    except Exception as e:
        return(e)
        
def update_rating(df, song_id, rating):
    try:
        for index, row in df.iterrows():
            if int(index)==int(song_id-1):
                df.loc[index, 'rating'] = rating

        return
    
    except Exception as e:
        return e

def get_song_lyrics(song_name):
    try:
        song = wiki.search_song(song_name=song_name, artist_name='')
        if song:
            lyrics = song.get_lyrics()
        
            return lyrics
        else:
            return False
    except Exception as e:
        return e
    
df = get_data(filePath=filePath)
items_per_page= 10


#API Calls
@app.route('/')
@app.route('/<int:page>')
def display_songs(page=1):
    songs = get_all_title(df)
    total_pages = math.ceil(len(songs) / items_per_page)
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    displayed_songs = songs[start_index:end_index]
    
    return render_template('index.html', songs=displayed_songs, total_pages=total_pages)

@app.route('/search', methods=['POST'])
def search_songs():
    songs = get_all_title(df)
    if request.form.get('searchInput', '').isdigit():
        search_term = str(request.form.get('searchInput', ''))
    else:
        search_term = request.form.get('searchInput', '').lower()
        
    filtered_songs = [song for song in songs if search_term in str(song).lower()]
    if filtered_songs:
        return render_template('index.html', songs=filtered_songs, total_pages=1)
    else:
        return render_template('song_not_found.html', type = 'Song')
    
    
@app.route('/song/<int:song_id>', methods=['GET'])
def get_song_details(song_id):
    details = get_song_by_id(df, song_id)
    return render_template('song_detail.html', details = details)

@app.route('/song/<int:song_id>/lyrics', methods=['GET'])
def get_lyrics(song_id):
    song = get_song_by_id(df, song_id)
    details = get_song_lyrics(song['title'])
    if details:
        return render_template('song_lyrics.html', details=details)
    else:
        return render_template('song_not_found.html', type = 'Lyrics')

@app.route('/song/<int:song_id>/rate', methods=['POST'])
def rate_song(song_id):
    rating = int(request.form.get('rating'))
    update_rating(df, song_id, rating)
    
    return redirect(url_for('display_songs'))
  
app.run(debug=True, port=5052)