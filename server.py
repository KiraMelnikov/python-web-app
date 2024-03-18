from flask import Flask, render_template, request
from waitress import serve
from geo_service_API import ConnectionsAPI as geoApi
try:
    from weather import Weather as w
except:
    ImportError('Not found module which is call: "weather"')

app = Flask(__name__, template_folder="templates")

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def getting_weather():
    city = request.args.get(key='city')

    # checking if city not found 
    if not bool(city.strip()):
        city = "Kyiv"
    weather_data = w.get_weather(city=city)

    # checking if city not found
    if not weather_data["cod"] == 200:
        return render_template('city-not-found.html')
    
    return render_template(
        'weather.html',
        title= weather_data['name'],
        status= weather_data['weather'][0]['description'],
        temp= f"{weather_data['main']['temp']:.1f}",
        feels_like= f"{weather_data['main']['feels_like']:.1f}"
    )

@app.route('/geo_km')
def geo_km():
    result = geoApi().get_request(50.467995,30.877765,49.754654,31.459351) 
    return render_template(
        'geo_km.html',
        var_km = str(result["trip"]["summary"]["length"]) + " km",
        var_cost = str(result["trip"]["summary"]["cost"]) + " cost",
        var_time = str(result["trip"]["summary"]["time"]) + " time"
        )

if __name__=='__main__':
    serve(app, host="0.0.0.0", port=8000)