from flask import Flask, render_template, request
import webbrowser
import threading
import requests

app = Flask(__name__)

API_KEY = 'f32736da6a8ad72407060e3375af698f'  # Replace with your OpenWeatherMap API key
#CITY = 'Los Angeles'  # Replace with your desired city

#f32736da6a8ad72407060e3375af698f

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f'{weather.capitalize()} with a temperature of {temperature}°F'
    else:
        return 'Unable to fetch weather data'

def get_time(city):
    months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    from datetime import datetime, timedelta, timezone
    """Returns the local time given a GMT offset in hours."""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        offset = timedelta(seconds=int(data['timezone']))
    now = datetime.now(timezone.utc) + offset
    period = 'AM'
    if now.hour > 12:
        hour = now.hour - 12
        period = 'PM'
    else:
        hour = now.hour
        period = 'AM'

    return f'{months[now.month]} {now.day}, {now.year} {hour}:{str(now.minute).zfill(2)}:{now.second} {period}'



@app.route('/')
def index():
    return render_template('weatherapp.html', weather='weather of selected city', city='selected city', time='time of selected city')

@app.route('/button_clicked', methods=['POST'])
def button_clicked():
    city = request.form.get('city')
    weather = get_weather(city)
    time = get_time(city)
    return render_template('weatherapp.html', weather=weather, city=city, time=time)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Start a thread to open the browser after a short delay
    threading.Timer(1, open_browser).start()
    app.run(debug=True)