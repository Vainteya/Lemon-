LITTLE LEMON WEB APPLICATION
Meta Back-End Developer Capstone Project
========================================

A Django + Django REST Framework back end for the Little Lemon restaurant:
a static home page, a menu API, an authenticated table-booking API, and
user registration / token login through Djoser.


1. REQUIREMENTS
---------------
- Python 3.10 or newer
- MySQL Server 8.x running on 127.0.0.1:3306


2. SETUP
--------
a) Create a virtual environment and install the dependencies
   (run from this folder, the one containing manage.py):

       python -m venv .venv
       .venv\Scripts\activate          (Windows)
       source .venv/bin/activate       (macOS / Linux)
       pip install -r requirements.txt

b) Create the MySQL database:

       mysql -u root -p -e "CREATE DATABASE littlelemon CHARACTER SET utf8mb4;"

c) Set your MySQL credentials. littlelemon/settings.py connects with:

       NAME=littlelemon  USER=root  PASSWORD=your_password
       HOST=127.0.0.1    PORT=3306

   Either replace 'your_password' in settings.py with your MySQL root
   password, or leave the file alone and set an environment variable:

       set DB_PASSWORD=<your password>           (Windows cmd)
       $env:DB_PASSWORD="<your password>"        (Windows PowerShell)
       export DB_PASSWORD=<your password>        (macOS / Linux)

   DB_NAME, DB_USER, DB_HOST and DB_PORT can be overridden the same way.

d) Apply the migrations:

       python manage.py migrate

e) (Optional) Create an admin user for /admin/ and /api/users/:

       python manage.py createsuperuser

f) Start the server:

       python manage.py runserver

   The home page is at http://127.0.0.1:8000/


3. RUNNING THE TESTS
--------------------
       python manage.py test

   Django creates a temporary MySQL database named "test_littlelemon", so the
   MySQL user needs permission to create databases (root has it).

   Tests live in restaurant/tests/:
     - test_models.py : MenuItemTest (str -> "IceCream : 80"), BookingTest
     - test_views.py  : MenuViewTest (GET /api/menu-items/ compared against
                        the serializer output), single-item CRUD, booking
                        auth, user list, and the register/login flow.


4. API ENDPOINTS (for Insomnia / Postman)
-----------------------------------------
Base URL: http://127.0.0.1:8000

Static page
  GET     /                          Little Lemon home page (index.html)

User registration and login (Djoser)
  POST    /auth/users/               Register a user
                                     body: {"username": "...", "password": "...", "email": "..."}
  POST    /auth/token/login/         Log in and get a token
                                     body: {"username": "...", "password": "..."}
                                     response: {"auth_token": "<token_key>"}
  POST    /auth/token/logout/        Invalidate the token (requires token header)
  GET     /auth/users/me/            Current user details (requires token header)

Menu items (reading is open to everyone; POST/PUT/PATCH/DELETE require the
token header "Authorization: Token <token_key>" and return 401 without it)
  GET     /api/menu-items/           List all menu items
  POST    /api/menu-items/           Create a menu item
                                     body: {"title": "Greek Salad", "price": "12.99", "inventory": 20}
  GET     /api/menu-items/<id>/      Retrieve a single menu item
  PUT     /api/menu-items/<id>/      Replace a menu item (all fields)
  PATCH   /api/menu-items/<id>/      Update some fields of a menu item
  DELETE  /api/menu-items/<id>/      Delete a menu item

  Validation: price must be >= 0, inventory must be 0-32767, and a booking's
  no_of_guests must be at least 1. Invalid values return 400 Bad Request.

Table bookings (token authentication REQUIRED)
  Header: Authorization: Token <token_key>
  GET     /api/bookings/             List all bookings
  POST    /api/bookings/             Create a booking
                                     body: {"name": "Alice", "no_of_guests": 4,
                                            "booking_date": "2026-11-01T19:30:00Z"}
  GET     /api/bookings/<id>/        Retrieve a booking
  PUT     /api/bookings/<id>/        Replace a booking
  PATCH   /api/bookings/<id>/        Update some fields of a booking
  DELETE  /api/bookings/<id>/        Delete a booking

  Without the header these return 401 Unauthorized.

Users (admin / staff only)
  GET     /api/users/                List users (url, username, email, groups)
  GET     /api/users/<id>/           Retrieve a user

Other
  GET     /api/                      DRF browsable API root
  GET     /api-auth/login/           DRF browsable API session login
  GET     /admin/                    Django admin (Booking and MenuItem registered)


5. SUGGESTED REVIEW FLOW
------------------------
  1. POST /auth/users/ to register.
  2. POST /auth/token/login/ and copy "auth_token" from the response.
  3. GET /api/menu-items/ with no header: expect 200.
  4. POST /api/menu-items/ with no header: expect 401.
  5. Add the header "Authorization: Token <auth_token>" and POST a few menu
     items, then GET /api/menu-items/ to see them.
  6. GET /api/bookings/ with no header: expect 401; with the header: expect 200.
  7. POST /api/bookings/ with the header to create a booking.


6. PROJECT STRUCTURE
--------------------
  littlelemon/
    manage.py
    Readme.txt
    requirements.txt
    littlelemon/             Django project (settings.py, urls.py)
    restaurant/              Django app
      models.py              Booking, MenuItem
      serializers.py         MenuItemSerializer, BookingSerializer, UserSerializer
      views.py               index, MenuItemsView, SingleMenuItemView,
                             BookingViewSet, UserViewSet
      urls.py                Home page, menu routes, DefaultRouter (bookings, users)
      admin.py
      migrations/
      templates/index.html
      static/css, static/js, static/img
      tests/
