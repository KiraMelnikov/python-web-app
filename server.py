from flask import Flask, render_template, request
from waitress import serve
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

if __name__=='__main__':
    serve(app, host="127.0.0.1", port=5500)