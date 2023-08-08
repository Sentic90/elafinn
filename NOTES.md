

<!-- DashBoard -->

<!-- Main -->
- hotels/hotel_detail/maka-hotel/orders/add/30
        order_add(request, slug, roomId)
        main/order-add.html
    
hotels/hotel_detail/<slug:slug>/orders/add/<int:roomId>/new
    order_create(request, slug, roomId)

    main/success_order.html