## TAKEWAY 
    - hotel.user.room_set.all()

## TODO 
### Seasons package active or disabled (done)
### filtering (done)
### User have to register create accounts (done)
### dashboard for customers (done)
### button disabled (done)
### Hotel details page 80% (done)
### Owner of rooms if rented (done)
### add year field to seasons (done)
### Orders -> Booking (done)

# Tasks
## Booking:
    - customers 
        - add booking
        - add guests & document upload 
        - upload payment receipt in case of ...
        - styling...
    - admins 
        - receive payment reciept file 
        - viewing document & data with readOnly property 
        - add Modal to edit a booking status..
        - Styling... 


##  filtering (working)
    - q1 = Q(city='Madinah')  // from Form
    - q2 = Q(nationality__contains='SA') // from form
    - q3 = 
    - qs.filter(q1 & q2) (Done)
            * filtering by city & nationality 

    - add rooms to Sessions 
    - matching nationality 
        - adding coutnries from Backend 
    - city Makkah | Madinah

    - Queries:
        rooms
        nationality
        datefilter:
            q1 = Q(start_date__lte=startDate, end_date__gte=startDate)
            q2 = Q(start_date__lte=endDate, end_date__gte=endDate)
            q3 = Q( start_date__gte=startDate, end_date__lte=endDate)
            Booking.objects.filter(q1 | q2 | q3).values_list('room_id', flat=True)

            # hotels without these booked rooms 
            available_hotels = Hotel.objects.(room__id__in=booked_room_ids)
            # to remove redundant 
            final_hotels = available_hotels.distinct()

        city

    - accommodate space 
        number of avaliable room

## Sidebar Filtering  (done)
    - filtering by distance
        - away from hrm 

    - filtering by Star count 
        - implementation 
        - 
    - filtering by prices 
        - implementation 
    
    - filtering by payment methods 
    - styling....


## Payment methods 
    - updating (done)
    - viewing (done)
    - adding from dashboard ...(done)
    - 



<!-- Models  -->
## Hotel:
    - user PK
    - hotel_name
    - city 
    - address
    - tel 
    - mobile 
    - category 
    - check_in
    - check_out
    - nationality
    - is_priority
    - slug

    # total_room
    # total_capacity
    # accomadate_space
    # rooms


## ROOM:
    - roomType
    - roomNo
    - floor
    - capacity
    - Electric
    - Facilities
    - Services
    - status
    - is_mine
    - hotel
    - is_view
    - created
    - updated
    - price

## TODO

    - season resrection to Ramdan package
    - add package to booking...
    - guests numbers 
    - rooms 