import requests
import os 
import json
from abc import ABC, abstractclassmethod
from dotenv import load_dotenv

load_dotenv()


class API(ABC):
    """ Abstract class Weather from API """

    @abstractclassmethod
    def get_attr ():
        pass

    @abstractclassmethod
    def set_attr ():
        pass

    @abstractclassmethod
    def get_weather():
        pass

    @abstractclassmethod
    def check_connect():
        return False

class Weather(API):
    """ Weather app from API """

    @staticmethod
    def check_connect(url: str) -> bool:
        """ Checking any connection by url """
        response = requests.get(url=url)
        if response.ok:
            return True

    @classmethod
    def get_weather(cls, city: str ='Kyiv') -> json:
        url = f'https://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&&units=metric'
        if cls.check_connect(url):
            try:
                response = requests.get(url=url).json()
                return response
            except:
                raise requests.RequestException("Somethink wrong with url")
        else:
            raise requests.ConnectionError("Connection was failed")


if __name__=='__main__':

    city = input("\nEnter the city\n")
    weather_data = Weather.get_weather(city)
    print(weather_data)
