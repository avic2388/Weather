from flask import Flask, render_template, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

def get_weather(city):
    """Отримати погоду з wttr.in для вказаного міста"""
    try:
        url = f"https://wttr.in/{city}?format=j1&lang=uk"
        response = requests.get(url)
        response.raise_for_status()  # Перевіряємо на помилки HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Помилка запиту до API: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if city:
            data = get_weather(city)
            
            if data:
                try:
                    current = data['current_condition'][0]
                    weather_data = {
                        'city': data['nearest_area'][0]['areaName'][0]['value'],
                        'temp': current['temp_C'],
                        'feels_like': current['FeelsLikeC'],
                        'description': current['lang_uk'][0]['value'],
                        'icon': current['weatherCode'],
                        'humidity': current['humidity'],
                        'wind': current['windspeedKmph'],
                        'pressure': current['pressure'],
                        'visibility': current['visibility'],
                        'time': datetime.now().strftime('%H:%M, %d.%m.%Y')
                    }
                except (KeyError, IndexError) as e:
                    error = "Помилка обробки даних погоди"
                    print(f"Помилка парсингу: {e}")
            else:
                error = f"Не вдалося отримати дані для міста '{city}'. Спробуйте ще раз."
    
    return render_template('index.html', weather=weather_data, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
