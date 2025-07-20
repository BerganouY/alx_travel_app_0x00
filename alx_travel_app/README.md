    # ALX Travel App

A comprehensive Django REST API for managing travel listings, bookings, and reviews.

## Features

- **Listings Management**: Create, read, update, and delete travel property listings
- **Category System**: Organize listings by categories
- **User Reviews**: Rate and review listings
- **Booking System**: Make and manage reservations
- **Image Upload**: Upload and manage listing images
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Search & Filtering**: Advanced search and filtering capabilities
- **Authentication**: Token-based authentication
- **CORS Support**: Cross-origin resource sharing enabled

## Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework
- **Database**: MySQL
- **Task Queue**: Celery with RabbitMQ
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Environment Management**: django-environ

## Installation

### Prerequisites

- Python 3.8+
- MySQL
- RabbitMQ (for Celery)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/alx_travel_app.git
   cd alx_travel_app
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Create MySQL database**
   ```sql
   CREATE DATABASE alx_travel_db;
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

## Running the Application

### Development Server
```bash
python manage.py runserver
```

### Celery Worker (in separate terminal)
```bash
celery -A alx_travel_app worker --loglevel=info
```

### Celery Beat (for scheduled tasks, in separate terminal)
```bash
celery -A alx_travel_app beat --loglevel=info
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Admin Interface**: http://localhost:8000/admin/

## API Endpoints

### Categories
- `GET /api/v1/categories/` - List all categories
- `POST /api/v1/categories/` - Create a new category
- `GET /api/v1/categories/{id}/` - Get category details
- `PUT /api/v1/categories/{id}/` - Update category
- `DELETE /api/v1/categories/{id}/` - Delete category
- `GET /api/v1/categories/{id}/listings/` - Get listings in category

### Listings
- `GET /api/v1/listings/` - List all listings (with filtering)
- `POST /api/v1/listings/` - Create a new listing
- `GET /api/v1/listings/{id}/` - Get listing details
- `PUT /api/v1/listings/{id}/` - Update listing
- `DELETE /api/v1/listings/{id}/` - Delete listing
- `GET /api/v1/listings/{id}/reviews/` - Get listing reviews
- `POST /api/v1/listings/{id}/add_review/` - Add review to listing
- `GET /api/v1/listings/{id}/check_availability/` - Check availability

### Reviews
- `GET /api/v1/reviews/` - List all reviews
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/{id}/` - Get review details
- `PUT /api/v1/reviews/{id}/` - Update review
- `DELETE /api/v1/reviews/{id}/` - Delete review

### Bookings
- `GET /api/v1/bookings/` - List user's bookings
- `POST /api/v1/bookings/` - Create a new booking
- `GET /api/v1/bookings/{id}/` - Get booking details
- `PUT /api/v1/bookings/{id}/` - Update booking
- `DELETE /api/v1/bookings/{id}/` - Delete booking
- `POST /api/v1/bookings/{id}/cancel/` - Cancel booking

### Listing Images
- `GET /api/v1/listing-images/` - List all images
- `POST /api/v1/listing-images/` - Upload new image
- `GET /api/v1/listing-images/{id}/` - Get image details
- `PUT /api/v1/listing-images/{id}/` - Update image
- `DELETE /api/v1/listing-images/{id}/` - Delete image

## Query Parameters

### Listings Filtering
- `category` - Filter by category ID
- `max_guests` - Filter by maximum guests
- `bedrooms` - Filter by number of bedrooms
- `bathrooms` - Filter by number of bathrooms
- `is_available` - Filter by availability
- `min_price` - Minimum price per night
- `max_price` - Maximum price per night
- `location` - Search by location
- `search` - Search in title, description, location, amenities
- `ordering` - Order by: price_per_night, created_at, title

### Example API Calls

```bash
# Get all listings with filtering
GET /api/v1/listings/?category=1&max_guests=4&min_price=100&max_price=500

# Search listings
GET /api/v1/listings/?search=beach&location=miami

# Check availability
GET /api/v1/listings/123/check_availability/?check_in=2024-12-01&check_out=2024-12-05
```

## Authentication

The API uses token-based authentication. To authenticate:

1. Obtain a token by sending POST request to `/api-auth/login/`
2. Include the token in the Authorization header: `Authorization: Token your-token-here`

## Project Structure

```
alx_travel_app/
├── alx_travel_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── listings/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
├── .env.example
└── README.md
```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations listings
```

### Loading Sample Data
```bash
python manage.py loaddata fixtures/sample_data.json
```

## Deployment

### Production Settings

1. Set `DEBUG=False` in `.env`
2. Configure proper `ALLOWED_HOSTS`
3. Set up a proper database
4. Configure static file serving
5. Set up SSL/HTTPS
6. Configure logging
7. Set up monitoring

### Docker Deployment (Optional)

```bash
# Build image
docker build -t alx-travel-app .

# Run container
docker run -p 8000:8000 alx-travel-app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please email support@alxtravel.local or create an issue in the GitHub repository.  