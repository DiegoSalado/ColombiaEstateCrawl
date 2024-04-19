import pandas as pd
from utils import get_extra_information, get_information
from tqdm import tqdm
import json
import sys
import ast


# process input
property_types = ast.literal_eval(sys.argv[1])
sell_or_rent = sys.argv[2]
extra_information = eval(sys.argv[3])
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


    

def main(property_types:list, sell_or_rent, extra_information, cities:list):
    for city in cities:
        data = pd.DataFrame()
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
                                    "size": "50"
                                }
                                
                                response = get_information(params)
                                data = pd.concat([data, pd.DataFrame(response['results'])])
                                n_properties = response['totalHits']
                                n_pages = n_properties//50 if n_properties%50==0 else n_properties//50 +1

                                for property in range(n_pages):                
                                    params = {
                                        "realEstateTypeList": type_,
                                        "realEstateBusinessList": sell_or_rent,
                                        "bathroomList": str(n_bathroom),
                                        "roomList": str(n_room) if type_ in ['apartment', 'house'] else None,
                                        "realEstateStatus": use_status,
                                        "city": city,
                                        "from": str((property+1)*300),
                                        "size": "50"
                                    }
                                    try:
                                        response = get_information(params)
                                        data = pd.concat([data, pd.DataFrame(response['results'])])
                                    except:
                                        print(params)
                                
        DIRECTORY_PATH = f'data/{city}_{property_types_str}_{sell_or_rent}_properties.csv'
        data.to_csv(DIRECTORY_PATH, index=False)

        if extra_information:
            try:
                data = pd.read_csv(DIRECTORY_PATH).drop_duplicates().reset_index()
            except:
                continue
            print('Dowloading extra information...')
            for index_ in tqdm(data.index):
                try:
                    full_information = get_extra_information(data.loc[index_, 'link'])
                    for feature, value in full_information.items():
                        data.loc[index_,feature] = value
                except:
                    pass
            data.to_csv(DIRECTORY_PATH, index=False)

    return None

if __name__ == '__main__':
    main(property_types, sell_or_rent, extra_information, cities)
