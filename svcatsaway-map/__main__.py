from optparse import OptionParser
from http.client import HTTPSConnection
from base64 import b64encode
from datetime import datetime, timedelta
import urllib.parse
import json
import requests

parser = OptionParser()
parser.add_option("-m", "--memair-api-key", dest="memair_api_key", help="memair api key", metavar="FILE")
parser.add_option("-s", "--shopify-api-key", dest="shopify_api_key", help="shopify api key", metavar="FILE")
parser.add_option("-p", "--shopify-api-password", dest="shopify_api_pass", help="shopify api password", metavar="FILE")
parser.add_option("-g", "--page-id", dest="page_id", help="shopify page id", metavar="FILE")
parser.add_option("-u", "--myshopify-url-prefix", dest="url_prefix", help="url_prefix", metavar="FILE")
(options, args) = parser.parse_args()

def collect_locations():
  one_week_ago = str(datetime.utcnow() - timedelta(days=7))
  query = '{Locations(first: 1000, order: timestamp_desc, from_timestamp: "' + one_week_ago + '") {timestamp lat lon}}'
  data = {
    'query' : query,
    'access_token': '5c6cfea9c02565bbd28867111bd5f85839a63199daa475f201abe1098988f18a'
  }
  r = requests.post("https://memair.com/graphql", data)
  response = json.loads(r.text)
  return response['data']['Locations']

def generate_body(location):
  return json.dumps({
    'page': {
        'id': options.page_id,
        'body_html': body_html(location)
    }
  })

def body_html(locations):
  current_location = locations.pop(0)

  heat_map_points = ''
  for location in locations:
    heat_map_points += "new google.maps.LatLng({lat}, {lon}), ".format(lat=location['lat'], lon=location['lon'])

  return """
    <style>
      #map {{
       height: 400px;
       width: 100%;
      }}
    </style>
    <div id="map"></div>
    <div id="timestamp"></div>
    <script>

      var map, heatmap, marker, latest_location;

      latest_location = {{lat: {lat}, lng: {lon}, timestamp: '{timestamp}'}};

      function initMap() {{
        map = new google.maps.Map(document.getElementById('map'), {{
          zoom: 13,
          center: latest_location
        }});

        heatmap = new google.maps.visualization.HeatmapLayer({{
          data: getPoints(),
          radius: 15,
          opacity: 1,
          map: map
        }});

        marker = new google.maps.Marker({{
          position: latest_location,
          animation: google.maps.Animation.DROP,
          map: map
        }})
      }}

      function getPoints() {{
        return [{heat_map_points}];
      }}

      function timeSince(date) {{

        var seconds = Math.floor((new Date() - date) / 1000);

        var interval = Math.floor(seconds / 31536000);

        if (interval > 1) {{
          return interval + " years";
        }}
        interval = Math.floor(seconds / 2592000);
        if (interval > 1) {{
          return interval + " months";
        }}
        interval = Math.floor(seconds / 86400);
        if (interval > 1) {{
          return interval + " days";
        }}
        interval = Math.floor(seconds / 3600);
        if (interval > 1) {{
          return interval + " hours";
        }}
        interval = Math.floor(seconds / 60);
        if (interval > 1) {{
          return interval + " minutes";
        }}
        return Math.floor(seconds) + " seconds";
      }}

      document.getElementById("timestamp").innerHTML = 'Last updated ' + timeSince(new Date(Date.parse(latest_location['timestamp']))) + ' ago. Note: this map will not update when we are stationary.';
    </script>
    <script async defer
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBrmtrrkEdR_z0z-hNIS4l5Zxx3cX2y7vI&libraries=visualization&callback=initMap">
    </script>
  """.format(
    lat=current_location['lat'],
    lon=current_location['lon'],
    timestamp=current_location['timestamp'],
    heat_map_points=heat_map_points
  )

def post_locations(locations):
  request_url = '/admin/pages/' + options.page_id + '.json'
  body = generate_body(locations)
  conn = HTTPSConnection(host=(options.url_prefix + ".myshopify.com"))
  userAndPass = b64encode((options.shopify_api_key + ':' + options.shopify_api_pass).encode('UTF-8')).decode('ascii')
  headers = { 'Content-Type': 'application/json', 'Authorization' : 'Basic %s' %  userAndPass }
  conn.request('PUT', request_url, headers=headers, body=body)
  res = conn.getresponse()
  data = res.read()
  conn.close()
  print(data)

locations = collect_locations()
post_locations(locations)
