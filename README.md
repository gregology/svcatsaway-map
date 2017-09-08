# svcatsaway-map
Displaying Memair location data on Shopify site

Get your Google Maps API key from the [Google API Console](https://console.developers.google.com/flows/enableapi?apiid=maps_backend,geocoding_backend,directions_backend,distance_matrix_backend,elevation_backend,places_backend&reusekey=true).

Create a Shopify maps template `page.map.liquid`

git clone this repo, grab the required api keys and then

`python svcatsaway-map -m MEMAIR-API-KEY -s SHOPIFY-API-KEY -p SHOPIFY-API-PASSWORD -g PAGE-ID`
