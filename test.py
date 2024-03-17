import requests
import os 
import json
from dotenv import load_dotenv

load_dotenv()
city = input("\nEnter city name:\n")
url = f'https://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&&units=metric'

response = requests.get(url=url).json()

print(json.dumps(response, indent=2))