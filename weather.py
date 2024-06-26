import requests
import os
import json
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()


class API(ABC):
    """ Abstract class Weather from API """

    @abstractmethod
    def get_attr ():
        pass

    @abstractmethod
    def set_attr ():
        pass

    @abstractmethod
    def get_weather():
        pass

    @abstractmethod
    def check_connect():
        return False

class Weather(API):
    """ Weather app from API """

    @staticmethod
    def check_connect() -> bool:
        """ Checking any connection by url """
        url_to_check = 'https://api.openweathermap.org/data/2.5/weather'
        try:
            response = requests.get(url=url_to_check)
            return response.ok
        except requests.RequestException:
            return False

    @classmethod
    def get_weather(cls, city: str ='Kyiv') -> json:
        """ Getting the weather data from API """
        url = f'https://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&&units=metric'

        if not cls.check_connect():
            try:
                response = requests.get(url=url).json()
                return response
            except:
                raise requests.RequestException("Somethink wrong with url")
        else:
            raise requests.ConnectionError("Connection was failed")


if __name__=='__main__':
    print(Weather.check_connect())
    city = input("\nEnter the city\n")
    if not bool(city.strip()):
        city = "Kyiv"
    weather_data = Weather.get_weather(city)
    print(json.dumps(weather_data, indent=2, ensure_ascii=False))
