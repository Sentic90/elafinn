/**
 * Notes:
 *    to add Layer corrdinate:
 *          - check the city if it's Makkah or Maddinah.
 *          - then make a var to hold the cordinate of selectedCity
 * 2023/08/28   Tasks 
 * Employee:
 *    - URLs list details (done)
 *    - Views List Details (done)
 *    - template (done)
 *    - models ...working
 * Invoices 
 *    - URLs list details (done)
 *    - Views List Details (done)
 *    - template (done)
 *    - models ...(done)
 * Expenses 
 *    - URLs list details 
 *    - Views List details 
 *    - template (done)
 *    - models ...etc 
 * Stocks 
 *    - URLs list details  (done)
 *    - Views List details (done)
 *    - template (done)
 *    - models ... (done) 
 * 
 * Reports
 *    - working with PDFs
 * 2023/08/24   Tasks 
 * Filtering Query
 *          q1 = Q(city='Madinah')  // from Form
    -       q2 = Q(nationality__contains='SA')
    -       q3 = Q(start_date__lte='startDate', )
    -       q4 = Q()
 * Fitler by city (done)
 * Filter by nationality (done)
 * filter by Room
 *  - search for In Room models with selected room type 
 *          - signle=single ...etc
 *          - get the roomQueryset = Room.objects.filter(status=2 + roomType__in=[''])
 *          - roomQueryset.values('id') # get ids of rooms 
 *          - in Hotel we need to loop over each hotel and find his room with given query
 * 
 * 
 * filter by date range.
 *  - I want to pick date from the backend by: 
 *          add hidden field populated with start date & end date 
 *          use jQuery to pick date from each tab (done)
 * 
 *          - Serach will be based on booking related to Hotel
 *                  we need to loop over each hotel & find his bookings
 *                  
 *          
 * 
 * 
 * 
 * 2023/08/23   Tasks 
 * Refactoring to main search views 
 *  - modifying QuerySet + Manager 
 *  - send the Query params to models 
 *  - ensure of search params and turnoff Buggy**
 * Request:
 *  - confirmation modal to Admin 
 * Price module 
 *  - jQuery looping ..working 
 * 
 *  - vat (Hotel) + prices (ROOMS) = totalPriceWithVat (done)
 * 2023/08/22   Tasks 
 * Add nationality to booking (done)
 * cancel Gender of Booker (done)
 * add notifications Model to customers (done)
 * customer get notified when request Has been accepted (done)
 * 
 * notifications (done)
 *  - models:   message time user is_Viewd
 * requests:
 *      - models (done)
 *      - Forms same as BookingForm (done)
 *      - views (done)
 *      - URLs (done)
 *      - template (done)
 *      - Signals ***IMPORTANT (done)
 *      - where the data of Booking go before confirmed. (done)
 *      - Request status (done)
 * 
 * Requests 
 *  - URLS -> list (GET + POST)+ details (GET + POST)
 */


/**
 * 
 * Save the package to be send in case of booking 
 * enhance filter by add dedicated sideFilter endpoint.
 * sidefilter 
 *  - intialize sidefilter-view & urls for it
 *  - start by initilaize queryset & then pass request.GET + queryset=queryset to hotelfilter
 *  - hotel_filter will returen obj set hotels = hotel_filter.qs --> return QuerySet
 *  - passed as context to template engine 
 *  - the data u need will finded in hidden fields 
 *  - use django-filter 
 *  - define filters.py 
 *  - define HotelFilter() class 
 *  - filter by stars count 
 *  - specifiy field that you wanna to filter with
 *  - 
 * Payment method for Hotel 
 * change Booking Status 
 *  - 
 * data of booking in admin-panel unchangable ... except status 
 * let customer to upload recipt of transaction amount
 * 
 */


/**
 *  booked_room_ids = Booking.objects.filter(
    Q(start_date__lte=start_date, end_date__gte=start_date) |  # Overlapping start date
    Q(start_date__lte=end_date, end_date__gte=end_date) |      # Overlapping end date
    Q(start_date__gte=start_date, end_date__lte=end_date)      # Fully contained within the range
        ).values_list("room__id", flat=True)

    # Filter the hotels based on rooms that are available
    available_hotels = Hotel.objects.exclude(room__id__in=booked_room_ids)

    # If you want the final list of hotels:
    final_hotels = available_hotels.distinct()
 */