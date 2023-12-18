from flask import request, render_template, redirect, url_for
from app import app, playlist
import math

@app.route('/')
@app.route('/<int:page>')
def display_songs(page=1):
    items_per_page= 10
    songs = playlist.get_all_title()
    total_pages = math.ceil(len(songs) / items_per_page)
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    displayed_songs = songs[start_index:end_index]
    
    return render_template('index.html', songs=displayed_songs, total_pages=total_pages)

@app.route('/search', methods=['POST'])
def search_songs():
    songs = playlist.get_all_title()
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
    details = playlist.get_song_by_id(song_id)
    return render_template('song_detail.html', details = details)

@app.route('/song/<int:song_id>/lyrics', methods=['GET'])
def get_lyrics(song_id):
    song = playlist.get_song_by_id( song_id)
    details = playlist.get_song_lyrics(song['title'])
    if details:
        return render_template('song_lyrics.html', details=details)
    else:
        return render_template('song_not_found.html', type = 'Lyrics')

@app.route('/song/<int:song_id>/rate', methods=['POST'])
def rate_song(song_id):
    rating = request.form.get('rating')
    playlist.update_rating(song_id, rating)
    
    return redirect(url_for('display_songs'))