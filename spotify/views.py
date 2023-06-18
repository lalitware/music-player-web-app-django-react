from django.shortcuts import render, redirect
from musicapp.settings import SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_ID, REDIRECT_URI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post
from .utils import update_or_create_user_token, is_spotify_authenticated, execute_spotify_api_request, play_or_pause_song, skip_to_next_song
from api.models import Room
from .models import Vote


# To provide authentication url to frontend.
# We are not sending the request directly to spotify here.
# We are just generating the url.
class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        # To prepare the url that will be requested by the frontend to authenticate.
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


# For redirection after spotify authentication and to get access token and refresh token.
# To send the request to spotify.
def spotify_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    # To send the post request to spotify to get access_token, refresh_token.
    response = post('https://accounts.spotify.com/api/token', data={
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_SECRET_ID,
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    # To check if the current user has an active session if not create it.
    if not request.session.exists(request.session.session_key):
        request.session.create()

    # call the update_or_create_user_token() function to update or create token data.
    update_or_create_user_token(
        request.session.session_key,
        refresh_token,
        access_token,
        expires_in,
        token_type,
    )

    # Redirect to home page of frontend app.
    return redirect('frontend:home')


# API view to check and update the authentication.
class CheckOrUpdateAuth(APIView):
    def post(self, request, format=None):
        # To check if user is authenticated or not.
        # If not then refresh the access token and update the token data in the db.
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key
        )

        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


# API view to get the current song,
class CurrentSong(APIView):
    def get(self, request, format=False):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)

        # To check if any room exists for the given room_code.
        if room.exists():
            room = room[0]
        else:
            return Response({'message': 'No Room Found!'}, status=status.HTTP_404_NOT_FOUND)

        host = room.host
        endpoint = 'player/currently-playing'
        response = execute_spotify_api_request(host, endpoint)

        if 'error' in response or 'item' not in response:
            # To handle response status cases
            if response.get('status') == 204:
                return Response(
                    {
                        'message': 'Spotify player is not active or song is not played yet since the app is opened!',
                        'status': '204',
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        'message': response.get('error').get('message'),
                        'status': response.get('error').get('status'),
                    },
                    status=response.get('error').get('status'),
                )

        # To check the whether the current playing item is song or not.
        if response.get('currently_playing_type') == "ad":
            return Response({'message': "Advertisement!", 'status': '204'}, status=status.HTTP_200_OK)
        if response.get('currently_playing_type') != "track":
            return Response(
                {
                    'message': "Only track should be played!",
                    'currently_playing_type': response.get('currently_playing_type'),
                    'status': '204'
                },
                status=status.HTTP_200_OK,
            )

        item = response.get('item')
        progress = response.get('progress_ms')
        is_playing = response.get('is_playing')
        song_id = item.get('id')
        duration = item.get('duration_ms')
        album_cover = item.get('album').get('images')[0].get('url')

        # To handle multiple artists case and to get the artists string.
        artist_string = ''
        for index, artist in enumerate(item.get('artists')):
            if index > 0:
                artist_string += ', '
            artist_string += artist.get('name')

        # To get all the votes for current song in the current room.
        votes_count = len(Vote.objects.filter(room=room, song_id=song_id))

        # Song info dict.
        song_info = {
            'id': song_id,
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'song_progress_time': progress,
            'is_playing': is_playing,
            'image_url': album_cover,
            'votes': votes_count,
            'votes_required': room.votes_to_skip,
        }

        # Method to update the song_id in Room model.
        self.update_room_current_song(song_id=song_id, room=room)

        return Response(song_info, status=status.HTTP_200_OK)

    # Method to update the song_id in Room model.
    def update_room_current_song(self, song_id, room):
        current_song = room.current_song
        # To check if current_song has the same current song_id
        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=['current_song'])

            # Remove all the votes to skip of the other songs
            votes = Vote.objects.filter(room=room)


# API view to play or pause the song.
class PlayOrPauseSong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get('room_code')
        play_or_pause_request = request.data.get('play_or_pause_request')
        rooms = Room.objects.filter(code=room_code)

        # To check if room exists.
        if rooms.exists():
            room = rooms[0]
            # To check for pause permission.
            if (self.request.session.session_key == room.host or room.guest_can_pause) and (play_or_pause_request == 'play' or play_or_pause_request == 'pause'):
                play_or_pause_song(room.host, play_or_pause_request)
                return Response({'message': 'Paused Successfully!'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Permission Denied!'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Room Not Found!'}, status=status.HTTP_204_NO_CONTENT)


# View for skip to the next song.
class SkipToNextSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get('room_code')
        rooms = Room.objects.filter(code=room_code)

        # To check if any room with given room_code exists
        if rooms.exists():
            room = rooms[0]

            # To get all the votes for current song in the current room.
            votes = Vote.objects.filter(room=room, song_id=room.current_song)

            # Host will skip the song without votes.
            if self.request.session.session_key == room.host:

                # Skip the song.
                response = skip_to_next_song(room.host)
                if response.get('error'):
                    return Response({'message': response.get('error').get('message')}, status=response.get('error').get('status'))
                else:
                    # Delete all the votes.
                    votes.delete()
                    return Response({'message': 'Song is skipped successfully!'}, status=status.HTTP_200_OK)
            else:  # Create a new vote object.
                # To check if the user is already voted.
                is_voted = Vote.objects.filter(
                    room=room, song_id=room.current_song, user=self.request.session.session_key).exists()
                if not is_voted:
                    vote = Vote(
                        user=self.request.session.session_key,
                        room=room,
                        song_id=room.current_song,
                    )
                    vote.save()

                    # To get all the votes for current song in the current room.
                    votes = Vote.objects.filter(
                        room=room,
                        song_id=room.current_song,
                    )

                    # skip the song if enough votes are met
                    votes_needed = room.votes_to_skip
                    if len(votes) >= votes_needed:
                        # Skip the song.
                        response = skip_to_next_song(room.host)
                        print(f"############## {response} ##############")
                        if response.get('error'):
                            return Response({'message': response.get('error').get('message')}, status=response.get('error').get('status'))
                        else:
                            # Delete all the votes.
                            votes.delete()
                            return Response({'message': 'Successfully Voted To Skip! and Song is skipped successfully!'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Successfully Voted To Skip!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Already Voted!'}, status=status.HTTP_200_OK)

        return Response({'message': 'Room Not Found!'}, status=status.HTTP_200_OK)
