from rest_framework import serializers
from .models import Room


# For rooms list get request.
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id',
            'code',
            'host',
            'guest_can_pause',
            'votes_to_skip',
            'created_at',
        )


# For create room post request.
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')


# For update room patch request.
class UpdateRoomSerializer(serializers.ModelSerializer):
    # As the code is unique field.
    # django will throw an error if we update the room object with the existing code.
    # To overcome this situation we are redefining this validation.
    code = serializers.CharField(validators=[]) 

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code')
