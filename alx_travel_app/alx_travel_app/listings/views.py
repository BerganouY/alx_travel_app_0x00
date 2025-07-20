from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Listing, ListingImage, Review, Booking
from .serializers import (
    CategorySerializer, ListingSerializer, ListingListSerializer,
    ListingImageSerializer, ReviewSerializer, BookingSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing categories."""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @swagger_auto_schema(
        operation_description="Get listings for a specific category",
        responses={200: ListingListSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def listings(self, request, pk=None):
        """Get all listings for a specific category."""
        category = self.get_object()
        listings = Listing.objects.filter(
            category=category,
            is_active=True,
            is_available=True
        )
        serializer = ListingListSerializer(listings, many=True, context={'request': request})
        return Response(serializer.data)


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing listings."""
    queryset = Listing.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'max_guests', 'bedrooms', 'bathrooms', 'is_available']
    search_fields = ['title', 'description', 'location', 'amenities']
    ordering_fields = ['price_per_night', 'created_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action == 'list':
            return ListingListSerializer
        return ListingSerializer

    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = super().get_queryset()

        # Price range filtering
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)

        # Location-based search
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(
                Q(location__icontains=location)
            )

        return queryset

    @swagger_auto_schema(
        operation_description="Get reviews for a specific listing",
        responses={200: ReviewSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific listing."""
        listing = self.get_object()
        reviews = Review.objects.filter(listing=listing, is_active=True)
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Add a review to a specific listing",
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer}
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        """Add a review for a specific listing."""
        listing = self.get_object()
        serializer = ReviewSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Check if user has already reviewed this listing
            existing_review = Review.objects.filter(
                listing=listing,
                reviewer=request.user
            ).first()

            if existing_review:
                return Response(
                    {'error': 'You have already reviewed this listing.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(listing=listing)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Check availability for specific dates",
        manual_parameters=[
            openapi.Parameter('check_in', openapi.IN_QUERY, description="Check-in date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('check_out', openapi.IN_QUERY, description="Check-out date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response('Availability status', openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    @action(detail=True, methods=['get'])
    def check_availability(self, request, pk=None):
        """Check if a listing is available for specific dates."""
        listing = self.get_object()
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')

        if not check_in or not check_out:
            return Response(
                {'error': 'Both check_in and check_out dates are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from datetime import datetime
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            listing=listing,
            status__in=['confirmed', 'pending'],
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        )

        is_available = not overlapping_bookings.exists() and listing.is_available

        return Response({
            'available': is_available,
            'check_in': check_in_date,
            'check_out': check_out_date,
            'listing_id': listing.id
        })


class ListingImageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing listing images."""
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter images by listing if provided."""
        queryset = super().get_queryset()
        listing_id = self.request.query_params.get('listing')
        if listing_id:
            queryset = queryset.filter(listing_id=listing_id)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing reviews."""
    queryset = Review.objects.filter(is_active=True)
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['listing', 'rating']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Set the reviewer to the current user."""
        serializer.save(reviewer=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing bookings."""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'listing']
    ordering_fields = ['check_in_date', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return bookings for the current user."""
        return Booking.objects.filter(guest=self.request.user)

    def perform_create(self, serializer):
        """Set the guest to the current user."""
        serializer.save(guest=self.request.user)

    @swagger_auto_schema(
        operation_description="Cancel a booking",
        responses={200: openapi.Response('Booking cancelled')}
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking."""
        booking = self.get_object()

        if booking.status in ['cancelled', 'completed']:
            return Response(
                {'error': f'Cannot cancel a {booking.status} booking.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'cancelled'
        booking.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data)