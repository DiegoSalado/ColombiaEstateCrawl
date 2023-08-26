import pandas as pd
from utils import get_coordinates, get_information
from tqdm import tqdm
import json
import sys
import ast


# process input
property_types = ast.literal_eval(sys.argv[1])
sell_or_rent = sys.argv[2]
coords = eval(sys.argv[3])
try:
    cities = ast.literal_eval(sys.argv[4])
    print(cities)
except:
    cities = ['Cartagena', 'Rionegro', 'Mosquera', 'Neiva', 'Barranquilla', 'Bello', 'Arbelaez', 'Ricaurte','Malambo',
            'Chía','Jamundí','Calera','Itaguí','Bucaramanga','Valledupar','Villavicencio','Funza',
            'Floridablanca','Palmira','Ibagué','Fusagasuga','Medellín','Cúcuta','Cajicá','Soacha','Tunja',
            'Cartago','Sogamoso','Anapoima','Zipaquirá','Envigado','Melgar','Villeta','Marta','Colombia','Madrid',
            'Soledad','Sopó','Cota','Pereira','Armenia','Sabaneta','Cali','Manizales','Bogotá','Tocancipá']


# set csv paths
cities_str = '_'.join(cities)
property_types_str = '_'.join(property_types)

if len(cities)==46:
    DIRECTORY_PATH = f'data/colombia_{property_types_str}_{sell_or_rent}_properties.csv'
else:
    DIRECTORY_PATH = f'data/{cities_str}_{property_types_str}_{sell_or_rent}_properties.csv'
    

def main(property_types:list, sell_or_rent, coords, cities:list):
    data = pd.DataFrame()
    for city in cities:
        for type_ in property_types:
            for use_status in ['nuevo', 'usado']:
                print(f'Dowloading all [{city}, {type_}, {use_status}]...')
                for n_bathroom in tqdm(range(1,6)):
                    for n_room in range(1,6):
                                if type_ not in ['apartamento','casa'] and n_room!=1:
                                    continue
                                params = {
                                    "realEstateTypeList": type_,
                                    "realEstateBusinessList": sell_or_rent,
                                    "bathroomList": str(n_bathroom),
                                    "roomList": str(n_room) if type_ in ['apartment', 'house'] else None,
                                    "realEstateStatus": use_status,
                                    "city": city,
                                    "from": "0",
                                    "size": "300"
                                }
                                
                                response = get_information(params)
                                data = pd.concat([data, pd.DataFrame(response['results'])])
                                n_properties = response['totalHits']
                                n_pages = n_properties//300 if n_properties%300==0 else n_properties//300 +1

                                for property in range(n_pages):                
                                    params = {
                                        "realEstateTypeList": type_,
                                        "realEstateBusinessList": sell_or_rent,
                                        "bathroomList": str(n_bathroom),
                                        "roomList": str(n_room) if type_ in ['apartment', 'house'] else None,
                                        "realEstateStatus": use_status,
                                        "city": city,
                                        "from": str((property+1)*300),
                                        "size": "300"
                                    }
                                    try:
                                        response = get_information(params)
                                        data = pd.concat([data, pd.DataFrame(response['results'])])
                                    except:
                                        print(params)
                                

    data.to_csv(DIRECTORY_PATH, index=False)

    if coords:
        data = pd.read_csv(DIRECTORY_PATH).drop_duplicates().reset_index()
        for index_ in tqdm(data.index):
            try:
                data.loc[index_, 'lat'], data.loc[index_, 'lon'] = get_coordinates(data.loc[index_, 'link'])
            except:
                pass
        data.to_csv(DIRECTORY_PATH, index=False)

    return None

if __name__ == '__main__':
    main(property_types, sell_or_rent, coords, cities)