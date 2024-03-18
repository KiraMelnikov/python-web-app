from geo_service_API import ConnectionsAPI as geoApi, ConnectionExeptions
import json
import pandas as pd
import numpy as np
import time

# var_km = result["trip"]["summary"]["length"]
# var_cost = result["trip"]["summary"]["cost"]
# var_time = result["trip"]["summary"]["time"]


def create_test_table() -> pd.DataFrame:
    """ Creating a test table """
    table = {'filial': [1, 2, 3, 4],
             'lat_from': [50.463959, 50.457995, 50.777995, 50.467895],
             'lon_from': [30.112205, 30.575885, 30.588205, 30.577205],
             'lat_to': [49.554654, 49.756354, 49.759854, 49.753654],
             'lon_to': [31.409351, 31.451351, 31.429351, 31.455351]
            }
    return pd.DataFrame(data=table)

def get_km(lat_from: float=0, lon_from: float=0, lat_to: float=0, lon_to: float=0) -> float:
    try:
        result = geoApi().get_request(lat_from, lon_from, lat_to, lon_to) 
    except:
        result = 0
        raise ConnectionExeptions("Something went wrong")
    else:
        return result["trip"]["summary"]["length"]
    finally:
        time.sleep(2) # restriction by time in second



def set_km(df:pd.DataFrame=create_test_table()) -> pd.DataFrame:
    for row in df.iterrows():
        df.loc[row[0],'distance (km)'] = get_km(row[1]["lat_from"],row[1]["lon_from"],row[1]["lat_to"],row[1]["lon_to"])
    return df

if __name__=='__main__':
    print(set_km())