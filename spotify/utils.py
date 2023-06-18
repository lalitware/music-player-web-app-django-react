from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from requests import Request, post, put, get
from musicapp.settings import SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_ID


# Spotify api base url.
SPOTIFY_BASE_URL = 'https://api.spotify.com/v1/me/'


# To get the user token data corrsponding to session_id from db.
def get_user_token_data(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


# To update or create the token data corresponding to a session_id.
def update_or_create_user_token(session_id, refresh_token, access_token, expires_in, token_type):
    token = get_user_token_data(session_id)

    # To store the actual time of token expiration.
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    # Update the token data if any token exists for session_id else create new token.
    if token:
        token.access_token = access_token
        token.expires_in = expires_in
        token.token_type = token_type
        token.save(update_fields=['access_token', 'expires_in', 'token_type'])
    else:
        token = SpotifyToken(
            user=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_in=expires_in
        )
        token.save()


# To check if user is authenticated or not.
def is_spotify_authenticated(session_id):
    token_data = get_user_token_data(session_id)
    if token_data:
        expiry = token_data.expires_in

        # To check if the token is expired
        # Token gets expired when expire time is less than the current time.
        if expiry <= timezone.now():
            # To refresh the access token and update the token data in the db.
            refresh_spotify_token(token_data, session_id)
        return True
    return False


# To refresh the access token and update the token data in the db.
def refresh_spotify_token(token_data, session_id):
    refresh_token = token_data.refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_SECRET_ID,
    }).json()

    # new access_token and refresh token.
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    update_or_create_user_token(
        session_id, refresh_token, access_token, expires_in, token_type)


# To send request to any spotify api endpoint.
def execute_spotify_api_request(session_id, endpoint, is_post_request=False, is_put_request=False):
    token_data = get_user_token_data(session_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token_data.access_token,
    }

    # To check the kind of request (post/put/get).
    if is_post_request:
        response = post(SPOTIFY_BASE_URL + endpoint, headers=headers)
    elif is_put_request:
        response = put(SPOTIFY_BASE_URL + endpoint, headers=headers)
    else:
        response = get(SPOTIFY_BASE_URL + endpoint, {}, headers=headers)

    try:
        return response.json()
    except:
        if response.status_code == 204:
            return {'message': 'No data!', 'status': response.status_code}
        else:
            return {'error': 'Issue with request', 'status': response.status_code}


# To play or pause song.
def play_or_pause_song(session_id, play_or_pause_request):
    return execute_spotify_api_request(session_id, f'player/{play_or_pause_request}', is_put_request=True)


# Function to skip to the next song.
def skip_to_next_song(session_id):
    return execute_spotify_api_request(session_id, 'player/next', is_post_request=True)
