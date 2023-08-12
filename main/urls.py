from django.urls import path, include

from . import views


app_name = "main"
urlpatterns = [

    path("", views.index, name="index"),
    path("hotels/", views.result, name="result"),
    path("home", views.home, name="home"),
    path("search", views.search_rooms, name="search"),
    path("search_room", views.search_rooms, name="room_search"),

    # hotels 
    path("hotels/hotel_detail/<slug:slug>/",
         views.hotel_details, name="hotel_detail"),
    
    # Rooms 
    path('hotels/hotel_detail/<slug:slug>/rooms/<int:roomId>', views.room_details, name='room-details'),
    # Handle Booking
    path("hotels/hotel_detail/<slug:slug>/booking/add/", views.booking_add, name="booking-add"),
    
    # Filters 
    path('filtered-sidebar/', views.filtered_sidebar, name='filtered-sidebar'),

    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    #
    # path('passwords_change/', views.change_password, name='change_password'),


]
