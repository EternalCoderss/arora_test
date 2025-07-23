from django.urls import path
from .views import AvailabilityView, BookingView, UserCreateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('availability/', AvailabilityView.as_view(), name='availability'),
    path('booking/', BookingView.as_view(), name='booking'),
]
