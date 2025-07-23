from rest_framework import generics
from rest_framework.permissions import AllowAny
from scheduler.models import UserAvailability, Booking
from django.contrib.auth.models import User
from .serializers import (
    UserAvailabilitySerializer,
    BookingSerializer,
    UserSerializer
)

# ------------------ USER CREATION ------------------

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 

# ------------------ AVAILABILITY ------------------

class AvailabilityView(generics.ListCreateAPIView):
    queryset = UserAvailability.objects.all()
    serializer_class = UserAvailabilitySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ------------------ BOOKING ------------------

class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
