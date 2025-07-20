# Django signals for the listings app
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Listing, Review, Booking


@receiver(post_save, sender=Listing)
def listing_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for when a listing is saved.
    Can be used for notifications, search indexing, etc.
    """
    if created:
        # Add any logic for newly created listings
        pass


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for when a review is saved.
    Can be used to update listing ratings, send notifications, etc.
    """
    if created:
        # Add any logic for new reviews
        pass


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for when a booking is saved.
    Can be used for notifications, calendar updates, etc.
    """
    if created:
        # Add any logic for new bookings
        pass


@receiver(pre_save, sender=Booking)
def booking_pre_save(sender, instance, **kwargs):
    """
    Signal handler for before a booking is saved.
    Can be used for validation, price calculation, etc.
    """
    # Calculate total price if not set
    if instance.listing and instance.check_in_date and instance.check_out_date:
        if not instance.total_price:
            duration = (instance.check_out_date - instance.check_in_date).days
            instance.total_price = duration * instance.listing.price_per_night