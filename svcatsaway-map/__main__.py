from optparse import OptionParser
from http.client import HTTPSConnection
from base64 import b64encode
import json

parser = OptionParser()
parser.add_option("-m", "--memair-api-key", dest="memair_api_key", help="memair api key", metavar="FILE")
parser.add_option("-s", "--shopify-api-key", dest="shopify_api_key", help="shopify api key", metavar="FILE")
parser.add_option("-p", "--shopify-api-password", dest="shopify_api_pass", help="shopify api password", metavar="FILE")
parser.add_option("-g", "--page-id", dest="page_id", help="shopify page id", metavar="FILE")
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
  return '{"page": {"id": ' + options.page_id + ', "body_html": "<script>var current_location = {lat: ' + str(location['lat']) + ', lng: ' + str(location['lon']) + '};</script>"}}'

def post_location(location):
  request_url = '/admin/pages/' + options.page_id + '.json'
  body = generate_body(location)
  c = HTTPSConnection(host="svcatsaway.myshopify.com")
  userAndPass = b64encode((options.shopify_api_key + ':' + options.shopify_api_pass).encode('UTF-8')).decode('ascii')
  headers = { 'Content-Type': 'application/json', 'Authorization' : 'Basic %s' %  userAndPass }
  c.request('PUT', request_url, headers=headers, body=body)
  res = c.getresponse()
  data = res.read()
  c.close()
  print(data)

location = collect_location()
post_location(location)
