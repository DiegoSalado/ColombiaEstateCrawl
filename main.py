from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from enums import DIRECTORY_PATH
from utils import get_coordinates, get_information
from tqdm import tqdm
import json
import sys
import ast

property_types = ast.literal_eval(sys.argv[1])
sell_or_rent = sys.argv[2]
coords = bool(sys.argv[3])
try:
    city = sys.argv[4]
except:
    city = None


def main(property_types:list, sell_or_rent='venta', coords=False, city=None):

    data = pd.DataFrame()
    for type_ in property_types:
        for use_status in ['nuevo', 'usado']:
            print(f'Dowloading all [{type_} {use_status}]...')
            for n_room in range(1,6):
                for n_bathroom in range(1,6):
                    for n_garage in range(6):
                        for stratum in range(1,9):
                            params = {
                                "realEstateTypeList": type_,
                                "realEstateBusinessList": sell_or_rent,
                                "bathroomList": str(n_bathroom),
                                "roomList": str(n_room),
                                "realEstateStatus": use_status,
                                "stratumList" : stratum,
                                "garageList" : n_garage if n_garage > 0 else None,
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
                                    "roomList": str(n_room),
                                    "realEstateStatus": use_status,
                                    "stratumList" : stratum,
                                    "garageList" : n_garage if n_garage > 0 else None,
                                    "city": city,
                                    "from": str((property+1)*300),
                                    "size": "300"
                                }
                                try:
                                    response = get_information(params)
                                    data = pd.concat([data, pd.DataFrame(response['results'])])
                                except:
                                    print(params)
            print(f'Done, dowloaded all [{type_} {use_status}]!')

    data.to_csv(DIRECTORY_PATH, index=False)

    if coords:
        data = pd.read_csv(DIRECTORY_PATH).drop_duplicates().reset_index()
        for index_ in tqdm(data.index):
            try:
                data.loc[index_, 'lat'], data.loc[index_, 'lon'] = get_coordinates(data.loc[index_, 'link'])
            except:
                print(index_)
                pass
        data.to_csv('../data/coords.csv', index=False)

    return None

if __name__ == '__main__':
    main(property_types, sell_or_rent, coords, city)