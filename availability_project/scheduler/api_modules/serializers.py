from rest_framework import serializers
from scheduler.models import UserAvailability, Booking
from datetime import datetime, date, timedelta
from django.contrib.auth.models import User

# ------------------- USER CREATION -------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# ------------------- USER AVAILABILITY -------------------

class UserAvailabilitySerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(help_text="Format: HH:MM:SS")
    end_time = serializers.TimeField(help_text="Format: HH:MM:SS")

    class Meta:
        model = UserAvailability
        fields = '__all__'

# ------------------- BOOKING -------------------

class BookingSerializer(serializers.ModelSerializer):
    start_time = serializers.TimeField(
        error_messages={'invalid': 'Invalid format. Use HH:MM:SS (24-hour).'}
    )
    end_time = serializers.TimeField(
        error_messages={'invalid': 'Invalid format. Use HH:MM:SS (24-hour).'}
    )

    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        slot_duration = (
            datetime.combine(date.min, data['end_time']) -
            datetime.combine(date.min, data['start_time'])
        )

        valid_durations = [timedelta(minutes=m) for m in [15, 30, 45, 60]]
        if slot_duration not in valid_durations:
            raise serializers.ValidationError("Slot must be 15, 30, 45 or 60 minutes long.")

        availability = data['availability']
        if not (availability.start_time <= data['start_time'] and availability.end_time >= data['end_time']):
            raise serializers.ValidationError("Slot is outside the available time range.")

        existing = Booking.objects.filter(
            availability=availability,
            date=data['date'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time']
        )
        if existing.exists():
            raise serializers.ValidationError("This slot overlaps with an existing booking.")

        return data
