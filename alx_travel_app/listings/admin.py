from django.contrib import admin
from .models import Category, Listing, ListingImage, Review, Booking


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created_at', 'updated_at']


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ['image', 'caption', 'is_primary', 'order']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'host', 'category', 'location',
        'price_per_night', 'max_guests', 'is_available',
        'is_active', 'created_at'
    ]
    list_filter = [
        'category', 'is_available', 'is_active',
        'created_at', 'max_guests', 'bedrooms'
    ]
    search_fields = ['title', 'description', 'location', 'host__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [ListingImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'host')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Property Details', {
            'fields': ('price_per_night', 'max_guests', 'bedrooms', 'bathrooms')
        }),
        ('Availability & Status', {
            'fields': ('is_available', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('amenities', 'house_rules', 'check_in_time', 'check_out_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'listing', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['listing__title', 'caption']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'listing', 'reviewer', 'rating', 'is_active', 'created_at'
    ]
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['listing__title', 'reviewer__username', 'comment']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'listing', 'guest', 'check_in_date',
        'check_out_date', 'number_of_guests', 'total_price',
        'status', 'created_at'
    ]
    list_filter = ['status', 'check_in_date', 'created_at']
    search_fields = ['listing__title', 'guest__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'check_in_date'
    fieldsets = (
        ('Booking Information', {
            'fields': ('listing', 'guest', 'status')
        }),
        ('Dates & Guests', {
            'fields': ('check_in_date', 'check_out_date', 'number_of_guests')
        }),
        ('Pricing', {
            'fields': ('total_price',)
        }),
        ('Additional Information', {
            'fields': ('special_requests',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Customize admin site headers
admin.site.site_header = "ALX Travel App Administration"
admin.site.site_title = "ALX Travel Admin"
admin.site.index_title = "Welcome to ALX Travel Administration"