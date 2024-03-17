import requests
import os 
from dotenv import load_dotenv

load_dotenv()

url = f'https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={os.getenv("API_KEY")}'

response = requests.get(url=url)

print(response.json())