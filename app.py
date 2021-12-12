from dotenv import dotenv_values
from urllib.parse import urlencode, parse_qs
from flask import Flask, url_for, render_template, redirect, request
import requests
import base64
import random
import os


'''
webapp_spotify/
	static/
		css/
		master.css
	templates/
		base.html
		login.html
	app.py
	.env
	README.md
'''

config = dotenv_values(".env")
client_id = config['CLIENT_ID']
client_secret = config['CLIENT_SECRET']
redirect_uri = config['REDIRECT_URI']
spotify_id = config['SPOTIFY_ID']


def generate_random_string(length):
    text = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    for i in range(length):
        text += possible[random.randint(0, len(possible) - 1)]
    return text


app = Flask(__name__)

page_data = {
    'title': 'Title',
    'user': {},
    'playlist': {},
    'tracks': {},
    'code': '',
    'output': '',
    'url': redirect_uri
}


@app.route('/')
def index():
    page_data['title'] = 'Welcome'
    return render_template('login.html', data=page_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    scope = 'user-read-private playlist-read-private'
    state = generate_random_string(16)
    return redirect('https://accounts.spotify.com/authorize?' + urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    }))


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    code = request.args.get('code')
    print('Code:', code, '\n')

    AUTH_URL = 'https://accounts.spotify.com/api/token/'
    AUTH_64 = base64.b64encode(
        (client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')

    form = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }
    headers = {
        'Authorization': 'Basic ' + AUTH_64,
        'Content-Type': 'application/x-www-form-urlencoded'

    }

    auth_response = requests.post(AUTH_URL, data=urlencode(
        form), headers=headers)
    auth_response_data = auth_response.json()
    if 'error' not in auth_response_data:
        access_token = auth_response_data['access_token']

        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token),
            'Content-Type': 'application/json'
        }

        BASE_URL = 'https://api.spotify.com/v1/'

        user = requests.get(BASE_URL + 'me/', headers=headers).json()

        playlist = requests.get(
            BASE_URL + 'playlists/' + spotify_id, headers=headers).json()
        tracks = playlist['tracks']

        if 'error' not in playlist:
            page_data['playlist'] = playlist
        if 'error' not in user:
            page_data['user'] = user
        if 'error' not in tracks:
            code_to_run = ""
            for i in range(len(tracks['items'])):
                track_name = tracks['items'][i]['track']['name']
                code_to_run += track_name.lower()
            code_to_run = code_to_run.replace("\\n", "\n")
            page_data['code'] = code_to_run
            with open('main.c', 'w') as f:
                f.write(code_to_run)
            try:
                os.system('gcc -o code main.c')
                out = os.popen('gcc -o code main.c && ./code').read()
                os.system('rm code main.c')
                page_data['output'] = out
            except Exception as e:
                raise

        else:
            print('Error ' + str(tracks['error']['status']) +
                  ': ' + str(tracks['error']['message']))

    return render_template("base.html", data=page_data)


if __name__ == '__main__':
    app.run()
