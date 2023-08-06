from django.urls import path, include

from . import views


app_name = "main"
urlpatterns = [

    path("", views.index, name="index"),
    path("hotels/", views.result, name="result"),
    path("home", views.home, name="home"),
    path("search", views.search_rooms, name="search"),
    path("search_room", views.search_rooms, name="room_search"),

    path("hotels/hotel_detail/<slug:slug>/",
         views.hotel_detail, name="hotel_detail"),
    path("hotels/hotel_detail/orders-add", views.order_add, name="order-add"),

    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    #
    # path('passwords_change/', views.change_password, name='change_password'),


]
