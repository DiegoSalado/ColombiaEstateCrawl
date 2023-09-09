import requests
import json
from enums import API_KEY

def get_information(params:dict):
  url = "https://www.metrocuadrado.com/rest-search/search"
  headers = {
    'x-api-key': API_KEY,
  }
  response = requests.request("GET", url, headers=headers, data={}, params=params, timeout=30)
  return response.json()

def get_extra_information(link:str):
  url = "https://www.metrocuadrado.com" + link
  response = requests.request("GET", url, timeout=10)
  data = response.text.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0]
  json_data = json.loads(data)
  coordinates = json_data['props']['initialState']['realestate']['basic']['coordinates']
  description = json_data['props']['initialProps']['pageProps']['realEstate']['comment']
  finishes = json_data['props']['initialProps']['pageProps']['realEstate']['featured']

  extra_information = {
    "lat" : coordinates['lat'], 
    "lon" : coordinates['lon'], 
    "description" : description,
    "extra_data" : str(data)
  }

  for finish in finishes:
    extra_information[finish['title']] = str(finish['items'])
    
  return extra_information