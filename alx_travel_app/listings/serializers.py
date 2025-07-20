from rest_framework import serializers
from .models import Listing, Booking, Review
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ListingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    listing = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'