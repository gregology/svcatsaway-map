# svcatsaway-map
Displaying Memair location data on Shopify site

Get your Google Maps API key from the [Google API Console](https://console.developers.google.com/flows/enableapi?apiid=maps_backend,geocoding_backend,directions_backend,distance_matrix_backend,elevation_backend,places_backend&reusekey=true).

Create a Shopify maps template `page.map.liquid`

```
<head>
  <style>
    #map {
      height: 400px;
      width: 100%;
    }
  </style>
</head>
<body>
  <div class="container main content main-wrapper">
    <div class="sixteen columns page clearfix">
      <h1 class="center">
        {{ page.title }}
      </h1>
      <div class="feature_divider"></div>

      <div id="map"></div>
      {% include 'page-multi-column', content: page.content %}
      <script>
        function initMap() {
          var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 8,
            center: current_location
          });
          var marker = new google.maps.Marker({
            position: current_location,
            map: map
          });
        }
      </script>
      <script async defer
              src="https://maps.googleapis.com/maps/api/js?key=YOURAPIKEY&callback=initMap">
      </script>

    </div>
  </div>
</body>
```
git clone this repo, grab the required api keys and then

`python svcatsaway-map -m MEMAIR-API-KEY -s SHOPIFY-API-KEY -p SHOPIFY-API-PASSWORD -g PAGE-ID`
