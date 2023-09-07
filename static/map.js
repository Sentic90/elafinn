$(document).ready(function () {
  

  // Coordinate of Makkah & Maddinah
  var MakkahCoordinate = {
    latitude: 21.423064802559917,
    longitude: 39.82498712936757,
  };
  var MadinahCoordinate = { latitude: 24.4672018, longitude: 39.6156392 };

  // Check the selected city
  var city = "{{ request.session.main_search_params.city}}";

  // Exract Selected City from Session
  var selectedCityCoordinate =
    city == "Makkah" ? MakkahCoordinate : MadinahCoordinate;

    // Initialize Map
    var map = L.map("map").setView(
    [selectedCityCoordinate.latitude, selectedCityCoordinate.longitude],
    13
  );

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  // Markers

  // const linkToHotel =
  //   '<a href="https://google.com/"><b>فندق انجم مكة!</b><br>يبعد ٢ كيلو.</a>';
  // marker.bindPopup(linkToHotel).openPopup();

    // Customer Icon
//   var myIcon = L.icon({
//     iconUrl: 'https://e7.pngegg.com/pngimages/760/399/png-clipart-map-computer-icons-flat-design-location-logo-location-icon-photography-heart.png',
//     iconSize: [38, 95],
//     iconAnchor: [22, 94],
//     popupAnchor: [-3, -76],
// });
  var hotels = [];
  $(".hotel-location-group").each(function () {
    hotels.push({
      name: $(this).find(".hotel-name").text(),
      long: $(this).find(".hotel-longitude").text(),
      lat: $(this).find(".hotel-latitude").text(),
    });
  });
  
  hotels.forEach((hotel) => {
    if (hotel.lat && hotel.long){
    L.marker([hotel.long, hotel.lat]).bindPopup(hotel.name).addTo(map).openPopup();}
  });
});
