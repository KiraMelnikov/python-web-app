from os import path, getenv, system, popen
from dotenv import load_dotenv
import requests
import json
from abc import ABC, abstractclassmethod
import urllib3
urllib3.disable_warnings()

load_dotenv()

class ConnectionExeptions(Exception):
    """Custom exception for connection issues."""


class API(ABC):
    """ Abstract class control """

    @abstractclassmethod
    def get_request():
        pass

    @abstractclassmethod
    def get_token():
        pass

    @abstractclassmethod
    def check_connect():
        pass


class ConnectionsAPI(API):
    """API GEO-SERVICE optimized for performance and readability."""

    def __init__(self):
        self.__TOKEN = self.get_token()
        self._URL = f'https://geo-public-api-qa.foodtech.team/v1/valhalla/route'
        self._HEADER = {'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.__TOKEN}' }
  
  
    @classmethod
    def get_token(cls) -> str:
        response = requests.post(
            "https://identity-public-qa.foodtech.team/connect/token",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': 'ecom--geo--qa',
                'client_secret': 'secret'
            }
        )
        response.raise_for_status()
        return response.json()["access_token"]


    def check_connect(self, params: str=None) -> bool:
        try:
            response = requests.get(self._URL, headers=self._HEADER, params={'json': json.dumps(params)})
            return response.ok
        except requests.RequestException:
            return False


    def get_request(self: object, lat_from: float, lon_from: float, lat_to: float, lon_to: float, tr_type: str = "car") -> json:  
        _PARAMS = {"locations":[{"lat":lat_from,"lon":lon_from},{"lat":lat_to,"lon":lon_to}],
                "costing":"auto",
                "costing_options":{
                                    "auto":{
                                        "country_crossing_penalty":2000.0
                                        }
                                    },
                "units":"kilometrs",
                "id":"route",
                "travel_type":f"{tr_type}"}           
        if self.check_connect(_PARAMS):
            try:
                response = requests.get(params={'json': json.dumps(_PARAMS)}, verify=False, headers=self._HEADER, url=self._URL)
            except:
                self.get_token()
                try:
                    response = requests.get(params={'json': json.dumps(_PARAMS)}, verify=False, headers=self._HEADER, url=self._URL)
                except:
                    raise ConnectionExeptions('GET request not found')
            else:              
                return response.json()
        else:
            raise ConnectionExeptions('Connection failed')
        

def status(func) -> str:
    def text ():
        print("\n\nProcessing >>>\n")
        func()
    return text

@status   
def Main():
    request1 = ConnectionsAPI()
    try:
        out = request1.get_request(50.467995,30.572205,49.754654,31.459351)
        print(out)
    except ConnectionExeptions as error:
        print(error)


if __name__=='__main__':
    Main()
