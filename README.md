# Scodify

Spotify playlists are the best IDE.



## Dependencies

Required:

```
gcc
python3
python3-flask
python3-dotenv
```


*Optional* (suggested):

```
python3-venv
```

## Setup

### Access to Spotify API

In order to use the Spotify API you need to set up the account as shown on [Spotify for Developers](https://developer.spotify.com/).
Register an application in the [Dashboard](https://developer.spotify.com/dashboard) and inside the app settings set a *redirect URI*, in this case **Flask** uses `http://127.0.0.1:5000`.

From there you will also get your *Client ID* and your *Client Secret*.



### Create `.env` file

Create a `.env` file in the project directory and set the following variables.

| **Name**        | **Value**     |
|-----------------|---------------|
| `CLIENT_ID`     | Client ID     |
| `CLIENT_SECRET` | Client Secret |
| `REDIRECT_URI`  | Redirect URI  |
| `SPOTIFY_ID`    | Spotify ID    |


The *Spotify ID* is the base-62 identifier that you usually can find at the end of a Spotify URL. It does not identify the type of resource, in order to make this program work you need it to be a **playlist** one.
You can get that identifier from a playlist URL, for example the *Spotify ID* of [this playlist](
https://open.spotify.com/playlist/3cEYpjA9oz9GiPac4AsH4n) is `3cEYpjA9oz9GiPac4AsH4n`.

## Run the application

```
cd scodify
```

*Suggested*:

```
python3 -m venv venv
. venv/bin/activate
```

*Optional*:

```
export FLASK_ENV=development
export FLASK_APP=app
```

Finally run with

```
flask run
```

or

```
python3 app.py
```


## Notes

This program is not case sensitive, all the text will be lowered.

In order to actually run the code you need white space separators, this program automatically replaces `'\\n'` with `'\n'`.

It will not handle errors and exceptions.

To be fair [that](https://open.spotify.com/playlist/5vfVQeT5Zwhwppar3gGzQ1) is the only playlist that actually compiles and runs.

