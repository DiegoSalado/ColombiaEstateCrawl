import requests
import json
from enums import API_KEY

def get_information(params:dict):
  url = "https://www.metrocuadrado.com/rest-search/search"
  headers = {
    'x-api-key': API_KEY,
  }
  response = requests.request("GET", url, headers=headers, data={}, params=params)
  return response.json()

def get_coordinates(link:str):
  url = "https://www.metrocuadrado.com" + link
  response = requests.request("GET", url, timeout=5)
  data = response.text.split('<script id="__NEXT_DATA__" type="application/json">')[1].split('</script>')[0]
  coordinates = json.loads(data)['props']['initialState']['realestate']['basic']['coordinates']
  return coordinates['lat'], coordinates['lon']
