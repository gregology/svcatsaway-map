from optparse import OptionParser
from http.client import HTTPSConnection
from base64 import b64encode
import json

parser = OptionParser()
parser.add_option("-m", "--memair-api-key", dest="memair_api_key", help="memair api key", metavar="FILE")
parser.add_option("-s", "--shopify-api-key", dest="shopify_api_key", help="shopify api key", metavar="FILE")
parser.add_option("-p", "--shopify-api-password", dest="shopify_api_pass", help="shopify api password", metavar="FILE")
parser.add_option("-g", "--page-id", dest="page_id", help="shopify page id", metavar="FILE")
parser.add_option("-u", "--myshopify-url-prefix", dest="url_prefix", help="url_prefix", metavar="FILE")
(options, args) = parser.parse_args()

def collect_location():
  c = HTTPSConnection(host='memair.herokuapp.com')
  headers = {"Content-type": "application/json"}
  c.request('GET', '/api/v1/locations', json.dumps({'access_token': options.memair_api_key, 'per_page': 1}), headers)
  content = c.getresponse()
  response = json.loads(content.read().decode('utf8'))
  c.close()
  print(response)
  return response['locations'][0]

def generate_body(location):
  return json.dumps({
    'page': {
        'id': options.page_id,
        'body_html': body_html(location)
    }
  })

def body_html(location):
    return """
      <style>
         #map {{
          height: 400px;
          width: 100%;
         }}
      </style>

      <h1 class="center">Our Current Location</h1>
      <div class="feature_divider"></div>

      <div id="map"></div>
      <div id="timestamp"></div>

      <script>
        var latest_location = {{lat: {lat}, lng: {lon}, timestamp: '{timestamp}'}};
        function initMap() {{
          var map = new google.maps.Map(document.getElementById('map'), {{
            zoom: 8,
            center: latest_location
          }});
          var marker = new google.maps.Marker({{
            position: latest_location,
            map: map
          }});
        }}
      </script>
      <script async defer
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBrmtrrkEdR_z0z-hNIS4l5Zxx3cX2y7vI&callback=initMap">
      </script>
      <script>
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
      </script>
      <script>
        document.getElementById("timestamp").innerHTML = 'Last updated ' + timeSince(new Date(Date.parse(latest_location['timestamp']))) + ' ago. Note: this map will not update when we are stationary.';
      </script>
    """.format(
      lat=location['lat'],
      lon=location['lon'],
      timestamp=location['timestamp'],
    )

def post_location(location):
  request_url = '/admin/pages/' + options.page_id + '.json'
  body = generate_body(location)
  c = HTTPSConnection(host=(options.url_prefix + ".myshopify.com"))
  userAndPass = b64encode((options.shopify_api_key + ':' + options.shopify_api_pass).encode('UTF-8')).decode('ascii')
  headers = { 'Content-Type': 'application/json', 'Authorization' : 'Basic %s' %  userAndPass }
  c.request('PUT', request_url, headers=headers, body=body)
  res = c.getresponse()
  data = res.read()
  c.close()
  print(data)

location = collect_location()
post_location(location)
