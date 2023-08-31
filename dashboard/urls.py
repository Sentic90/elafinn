from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     # statistics data
     path('dashboard/my_hotel/<slug:slug>/statistics', views.get_statistics_data, name='get-statistics-data'),
    
    # path('signup/', views.signup, name='signup'),
    # path('signup_clinic/', views.signup_clinic, name='signup_clinic'),
    #
    # path('passwords_change/', views.change_password, name='change_password'),

    path('dashboard/my_hotel/', views.my_hotel, name='my-hotel'),
    path('dashboard/my_hotel/edit/status/<int:hotelId>',
         views.change_hotel_status, name='change_status'),

    path('dashboard/my_hotel/add', views.add_hotel, name='add-hotel'),
    path('dashboard/my_hotel/<slug>',
         views.HotelDashboard.as_view(), name='hotel_dashboard'),

    path('dashboard/my_hotel/<slug>/information',
         views.HotelInformation.as_view(), name='hotel_information'),
    # path('dashboard/my_hotel/<slug>/location', views.show_location, name='show_location'),
    path('dashboard/my_hotel/<slug:slug>/hotel_current_location/', views.CurrentLocation.as_view(),
         name='hotel_current_location'),
    path('dashboard/my_hotel/<slug:slug>/hotel_current_location/<int:pk>', views.UpdateHotelLocation.as_view(),
         name='update_hotel_location'),
    path('dashboard/my_hotel/<slug:slug>/location',
         views.AddHotelLocation.as_view(), name='hotel_location'),

    path('dashboard/my_hotel/<slug>/hotel_gallery',
         views.hotel_gallery, name='hotel_gallery'),
    path('dashboard/my_hotel/<slug>/hotel_gallery/upload',
         views.HotelImage.as_view(), name='hotel_image'),
    path('dashboard/my_hotel/<slug>/hotel_gallery/add',
         views.gallery_upload, name='add_hotel_gallery'),
    path('dashboard/my_hotel/<slug>/hotel_gallery/upload',
         views.hotel_upload_images, name='hotel_upload_images'),

    path('dashboard/my_hotel/<slug:slug>/bookings',
         views.bookings, name='booking-list'),
    path('dashboard/my_hotel/<slug:slug>/bookings/add',
         views.booking_add, name='booking-add'),
    path('dashboard/my_hotel/<slug:slug>/bookings/edit/<int:bookingId>',
         views.booking_edit, name='booking-edit'),

    # Requests
    path('dashboard/my_hotel/<slug:slug>/requests',
         views.requests, name='request-list'),

    path('dashboard/my_hotel/<slug:slug>/requests/edit/<int:requestId>',
         views.request_details, name='request-details'),

    path('dashboard/my_hotel/<slug:slug>/rooms-list',
         views.room_list, name='room-list'),
    path('dashboard/my_hotel/<slug:slug>/rooms-grid',
         views.room_grid, name='room-grid'),
    path('dashboard/my_hotel/<slug:slug>/room-list/<int:pk>', views.RoomDetailView.as_view(),
         name='room_detail'),
    path('dashboard/my_hotel/<slug:slug>/rooms-list/add',
         views.CreateRoomView.as_view(), name='add-room'),

    path('dashboard/my_hotel/<slug:slug>/room-type',
         views.RoomTypeView.as_view(), name='room-type'),
    path('dashboard/my_hotel/<slug:slug>/room-type/<int:pk>', views.RoomTypeDetailView.as_view(),
         name='room_type_detail'),
    path('dashboard/my_hotel/<slug:slug>/room-type/add',
         views.CreateRoomTypeView.as_view(), name='add_room_type'),

    path('dashboard/my_hotel/<slug:slug>/season-price-list',
         views.season_price_list, name='season-price-list'),
    path('dashboard/my_hotel/<slug:slug>/season-price-list/<int:pk>', views.SeasonPriceDetailView.as_view(),
         name='season_price_detail'),
    path('dashboard/my_hotel/<slug:slug>/price/season-price-list/add', views.CreateSeasonPriceView.as_view(),
         name='add-season-price'),

    path('dashboard/my_hotel/<slug:slug>/annual_rent/list',
         views.rooms_for_annual_rent, name='annual_rent'),
    path('dashboard/my_hotel/<slug:slug>/annual_rent/list/<int:pk>',
         views.AnnualRentView.as_view(), name='update_annual_rent'),
    path('dashboard/my_hotel/<slug:slug>/annual_rent/list/add',
         views.AnnualRentAddView.as_view(), name='add_annual_rent'),

    # Employee
    path('dashboard/my_hotel/<slug:slug>/employee/employee-list',
         views.employee_list, name='employee-list'),
    path('dashboard/my_hotel/<slug:slug>/employee/employee/<int:employeeId>/update',
         views.employee_update, name='employee-update'),

    # Invoice
    path('dashboard/my_hotel/<slug:slug>/invoice/invoice-list',
         views.invoice_list, name='invoice-list'),
    path('dashboard/my_hotel/<slug:slug>/invoice/<int:invoiceId>/view',
         views.invoice_details, name='invoice-details'),
    path('dashboard/my_hotel/<slug:slug>/invoice/<int:invoiceId>/print',
         views.invoice_print, name='invoice-print'),

    # expense
    path('dashboard/my_hotel/<slug:slug>/expense/expense-list',
         views.expense_list, name='expense-list'),
    path('dashboard/my_hotel/<slug:slug>/expense/<int:expenseId>/view',
         views.expense_details, name='expense-details'),
    path('dashboard/my_hotel/<slug:slug>/expense/<int:expenseId>/print',
         views.expense_print, name='expense-print'),

    # Reports
     #  expense
    path('dashboard/my_hotel/<slug:slug>/report/expense-list',
         views.report_expense, name='report-expenses'),
     path('dashboard/my_hotel/<slug:slug>/report/stock/<int:expenseId>/update',
         views.report_expense_update, name='report-expense-update'),

     # Stock
    path('dashboard/my_hotel/<slug:slug>/report/stock-list',
         views.report_stock, name='report-stocks'),
    path('dashboard/my_hotel/<slug:slug>/report/stock/<int:stockId>/update',
         views.report_stock_update, name='report-stock-update'),

    # customer
    path('dashboard/my_hotel/<slug:slug>/customer/customer-list',
         views.customer, name='customer-list'),

    path('dashboard/my_hotel/<slug:slug>/payment/methods',
         views.payment_methods, name='payment-methods'),
    path('dashboard/my_hotel/<slug:slug>/payment/methods/<int:paymentMethodId>/edit',
         views.payment_method_edit, name='payment-methods-edit'),
]
