from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # To check if the current user has an active session if not create it.
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        # To check the post data that will come from frontend in the form of serilized json.
        serializer = self.serializer_class(data=request.data)
        # check for valid data.
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key

            # To check if any room exist for the same session_key upadate the room fields else create new room.
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                # To store the room code in the seession
                # To know the user's joined room
                self.request.session['room_code'] = room.code
            else:
                room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                )
                room.save()
                # To store the room code in the seession
                # To know the user's joined room
                self.request.session['room_code'] = room.code

            # Serialze the room data just created and send the response.
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid Data!'}, status=status.HTTP_400_BAD_REQUEST)


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        # To get the code parameter from the url.
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                # To assign bollean value by checking if the current user is host or not.
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Room code not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        # To check if the current user has an active session if not create it.
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                # To store the room code in the seession
                # To know the user's joined room
                self.request.session['room_code'] = code

                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)

            return Response({'Room Not Found': 'Invalid Room Code!'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'Bad Request': 'Invalid post data, did not find code key!'},
            status=status.HTTP_400_BAD_REQUEST
        )


# To check if the user has any active music room.
class UserInRoom(APIView):
    def get(self, request, format=None):
        # To check if there is any session exists.
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }

        return JsonResponse(data, status=status.HTTP_200_OK)


# To leave the music room.
class LeaveRoom(APIView):
    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            # To remove the room_code from session
            self.request.session.pop('room_code')

            # If the user is host then remove the entire room.
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()

        return Response({'Message': 'Success'}, status=status.HTTP_200_OK)


# To update the room settings.
class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        # To check if the current user has an active session if not create it.
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        # To check the data came from frontend is valid serilized json.
        serializer = self.serializer_class(data=request.data)
        # check for valid data.
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')
            
            # To check if any room exists for the given code. 
            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'Message': 'Room Not Found!'}, status=status.HTTP_404_NOT_FOUND)

            room = queryset[0]
            user_id = self.request.session.session_key
            # To check if the current user is host or not.
            if room.host != user_id:
                return Response({'Message': 'You are not the host of this room!'}, status=status.HTTP_403_FORBIDDEN)
            
            # To update the room data.
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid Data Entered!'}, status=status.HTTP_400_BAD_REQUEST)
