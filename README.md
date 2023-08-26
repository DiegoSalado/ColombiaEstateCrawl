# ColombiaEstateCrawl

ColombiaEstateCrawl is a data scraping project focused on gathering valuable information about real estate properties in Colombia.

This repository extrac data from [Metrocuadrado](https://www.metrocuadrado.com/) a Colombian real estate website that provides property listings and information.
Metrocuadrado contains listings of various types of properties, including apartments, houses, commercial spaces, and land for sale or rent.

## Use

This repository operates by running the *'main.py'* script and specifying the following arguments: *'list_properties_type'*, *'sell_or_rent'*, *'coords'*, and *'list_cities'*.

| Parameter  | Values | Description |
|---------------------|----------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| list_properties_type| `['apartamento','casa','oficina','local','bodega','lote','finca','consultorio','edificio-de-oficinas','edificio-de-apartamentos']` | Allowed values for property types. |
| sell_or_rent  | `'vent'` or `'renta'`  | Indicates whether the property is for sale or for rent.|
| coords  | `True` or `False`| If you choose `True`, all property listings will include geographical coordinates (latitude and longitude) for precise location data. This option is useful for mapping and spatial analysis purposes. Please note that selecting `True` might significantly increase the extraction time due to the additional data retrieval process. |
| list_cities  | ['Cartagena', 'Rionegro', 'Mosquera', 'Neiva', 'Barranquilla', 'Bello', 'Arbelaez', 'Ricaurte','Malambo','Chía','Jamundí','Calera','Itaguí','Bucaramanga','Valledupar', 'Villavicencio','Funza', 'Floridablanca','Palmira','Ibagué','Fusagasuga','Medellín','Cúcuta','Cajicá','Soacha','Tunja', 'Cartago','Sogamoso','Anapoima','Zipaquirá','Envigado','Melgar','Villeta','Marta','Colombia','Madrid', 'Soledad','Sopó','Cota','Pereira','Armenia','Sabaneta','Cali','Manizales','Bogotá', 'Tocancipá'] | If not specified, information will be extracted for all cities on the site.|

```
$ python main.py  "list_properties_type"  sell_or_rent    coords   "list_cities"
```

#### Example

```
$ python main.py "['casa']" venta True "['Medellín']"
```


### Warning

The ColombiaEstateCrawl repository provides information and tools for educational and research purposes to demonstrate techniques for web data scraping related to real estate information in Colombia. The repository does not store, distribute, or provide access to any actual data collected from websites.

The methods and code snippets shared in this repository are intended to showcase the process of responsibly collecting data from publicly available online sources. Users are cautioned that web scraping might be subject to legal and ethical considerations, and it is their responsibility to ensure compliance with applicable laws and website terms of use.

The creators and maintainers of ColombiaEstateCrawl do not endorse or encourage any unauthorized use or scraping of websites that may infringe upon the terms of those websites or violate any laws. Users of this repository are solely responsible for their actions and the way they apply the knowledge provided here.

By accessing and using ColombiaEstateCrawl, you acknowledge that the repository is designed solely to provide educational insights into web scraping techniques. The creators and maintainers of this repository disclaim any liability for the actions or consequences resulting from the use of the information, code, or techniques described herein.

Please use the information and techniques from ColombiaEstateCrawl responsibly, ensuring that your actions align with legal and ethical standards.