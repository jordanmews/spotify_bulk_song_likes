
from os import environ
import spotipy
from spotipy.oauth2 import SpotifyOAuth

environ.setdefault('SPOTIPY_CLIENT_ID','placeholder')
environ.setdefault('SPOTIPY_CLIENT_SECRET','placeholder')
environ.setdefault('SPOTIPY_REDIRECT_URI','http://localhost:8888/callback')
my_user_id='placeholder'

redir=environ.get('SPOTIPY_REDIRECT_URI')
scope = ["user-library-modify",'user-library-read','playlist-modify-private','playlist-modify-public']
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def enum_playlists(uid=my_user_id, save=False):
    playlists = sp.user_playlists(uid)
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            tracks = sp.playlist_tracks(playlist['id'])
            to_like = []

            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
            for i in tracks['items']:
                if len(to_like) < 50:
                    print('\t\t',i['track']['artists'][0]['name'], ' - ', i['track']['name'], 'xxx ',i['track']['id'])
                    to_like.append( i['track']['id'])
            if save:
                sp.current_user_saved_tracks_add(to_like)
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

def save_tracks_from_spotify_playlists():
    enum_playlists(uid='spotify',save=True)

genres = [
'acoustic',
'afrobeat',
'alt-rock',
'alternative',
'ambient',
'anime',
'black-metal',
'bluegrass',
'blues',
'bossanova',
'brazil',
'breakbeat',
'british',
'cantopop',
'chicago-house',
'children',
'chill',
'classical',
'club',
'comedy',
'country',
'dance',
'dancehall',
'death-metal',
'deep-house',
'detroit-techno',
'disco',
'disney',
'drum-and-bass',
'dub',
'dubstep',
'edm',
'electro',
'electronic',
'emo',
'folk',
'forro',
'french',
'funk',
'garage',
'german',
'gospel',
'goth',
'grindcore',
'groove',
'grunge',
'guitar',
'happy',
'hard-rock',
'hardcore',
'hardstyle',
'heavy-metal',
'hip-hop',
'holidays',
'honky-tonk',
'house',
'idm',
'indian',
'indie',
'indie-pop',
'industrial',
'iranian',
'j-dance',
'j-idol',
'j-pop',
'j-rock',
'jazz',
'k-pop',
'kids',
'latin',
'latino',
'malay',
'mandopop',
'metal',
'metal-misc',
'metalcore',
'minimal-techno',
'movies',
'mpb',
'new-age',
'new-release',
'opera',
'pagode',
'party',
'philippines-opm',
'piano',
'pop',
'pop-film',
'post-dubstep',
'power-pop',
'progressive-house',
'psych-rock',
'punk',
'punk-rock',
'r-n-b',
'rainy-day',
'reggae',
'reggaeton',
'road-trip',
'rock',
'rock-n-roll',
'rockabilly',
'romance',
'sad',
'salsa',
'samba',
'sertanejo',
'show-tunes',
'singer-songwriter',
'ska',
'sleep',
'songwriter',
'soul',
'soundtracks',
'spanish',
'study',
'summer',
'swedish',
'synth-pop',
'tango',
'techno',
'trance',
'trip-hop',
'turkish',
'work-out',
'world-music']

def add_all_categories(genres=genres):
    for cats in range(0, len(pp),5):
        print( genres[cats:cats+5])
        vv = genres[cats:cats+5]
        for i in range(0,10):

            t = [x for x in sp.recommendations(seed_genres=vv,limit=100)['tracks']]
            [print(x['name']) for x in t]
            t = [x['id'] for x in t]
            sp.current_user_saved_tracks_add(t[:50])
            sp.current_user_saved_tracks_add(t[50:])

def get_artists_ids(search='the beatles', like_related=False, type='artist'):
    if like_related:
        out = [(x['name'],x['id']) for x in sp.search(search, type=type, )['artists']['items']]
    else:
        ai = sp.search(search, type=type, )['artists']['items']
        out= [(ai[0]['name'],ai[0]['id'])]
    from pprint import pprint
    pprint(out)
    return out

def get_all_artist_albums(aid):
    return [x['id'] for x in sp.artist_albums(artist_id=aid)['items']]

def get_album_tracks(aid):
    return [x['id'] for x in sp.album_tracks(aid)['items']]

def like_tracks(tids):
    sp.current_user_saved_tracks_add(tids)

def like_all_tracks_by_artist(artist, like_related=False):
    artist_ids = get_artists_ids(artist,like_related)

    for a in artist_ids:
        albums = get_all_artist_albums(a[1])
        tracks = []
        [tracks.extend(get_album_tracks(x)) for x in albums]
        for x in range(0, len(tracks), 50):
            like_tracks(tracks[x:x+49])

def like_top10_tracks_by_artist(artist, like_related=False):
    artist_ids = get_artists_ids(artist,like_related)
    for a in artist_ids:
        tracks = [x['id'] for x in sp.artist_top_tracks(a[1])['tracks']]
        for x in range(0, len(tracks), 50):
            like_tracks(tracks[x:x+49])


def get_saved_track_artists():
    # iterate over saved tracks 50 at a time, pulling out unique artists
    unique_artists = []
    for a in range(0, sp.current_user_saved_tracks(limit=1)['total'], 50):
        t = sp.current_user_saved_tracks(limit=50,offset=a)
        for x in t['items']:
            for art in x['track']['artists']:
                artist_id = art['id']
                unique_artists.append(artist_id)
    return set(unique_artists)


# enum_playlists()
# add_all_categories()
# x = get_saved_track_artists()
# print('savedartists')
# print(x)
# like_top10_tracks_by_artist('dearly beloved',like_related=True)
# like_all_tracks_by_artist('dearly beloved',like_related=True)


# like_all_tracks_by_artist('iron & wine', True)
# like_all_tracks_by_artist('red hot chili peppers', True)
# save_tracks_from_spotify_playlists()