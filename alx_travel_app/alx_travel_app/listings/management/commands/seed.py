from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
import random
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        self.create_users()
        self.create_listings()
        self.create_bookings()
        self.create_reviews()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def create_users(self):
        if not User.objects.filter(email='owner@example.com').exists():
            User.objects.create_user(
                username='owner1',
                email='owner@example.com',
                password='testpass123'
            )

        if not User.objects.filter(email='guest@example.com').exists():
            User.objects.create_user(
                username='guest1',
                email='guest@example.com',
                password='testpass123'
            )

    def create_listings(self):
        owner = User.objects.get(email='owner@example.com')
        listings_data = [
            {
                'title': 'Beautiful Apartment in Downtown',
                'description': 'A cozy apartment with great views',
                'address': '123 Main St, Cityville',
                'property_type': 'APARTMENT',
                'price_per_night': 120.00,
                'bedrooms': 2,
                'bathrooms': 1,
                'max_guests': 4,
                'amenities': 'WiFi, Kitchen, TV, Parking'
            },
            {
                'title': 'Luxury Villa with Pool',
                'description': 'Spacious villa perfect for families',
                'address': '456 Beach Rd, Seaview',
                'property_type': 'VILLA',
                'price_per_night': 350.00,
                'bedrooms': 4,
                'bathrooms': 3,
                'max_guests': 8,
                'amenities': 'Pool, WiFi, Kitchen, AC, Parking'
            },
            {
                'title': 'Cozy Cabin in the Woods',
                'description': 'Perfect getaway in nature',
                'address': '789 Forest Ln, Mountainview',
                'property_type': 'CABIN',
                'price_per_night': 95.00,
                'bedrooms': 1,
                'bathrooms': 1,
                'max_guests': 2,
                'amenities': 'Fireplace, Kitchen, Hiking trails'
            }
        ]

        for listing_data in listings_data:
            Listing.objects.get_or_create(owner=owner, **listing_data)

    def create_bookings(self):
        guest = User.objects.get(email='guest@example.com')
        listings = Listing.objects.all()

        for listing in listings:
            start_date = datetime.now() + timedelta(days=random.randint(1, 30))
            end_date = start_date + timedelta(days=random.randint(1, 14))
            total_price = (end_date - start_date).days * listing.price_per_night

            Booking.objects.get_or_create(
                listing=listing,
                user=guest,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price
            )

    def create_reviews(self):
        guest = User.objects.get(email='guest@example.com')
        bookings = Booking.objects.all()

        for booking in bookings:
            Review.objects.get_or_create(
                listing=booking.listing,
                user=guest,
                rating=random.randint(3, 5),
                comment=f"Great stay at {booking.listing.title}! Would recommend."
            )