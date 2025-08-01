from flask import Flask, render_template, request
import requests
from datetime import datetime
import os  # Додано імпорт os для роботи з змінними середовища

app = Flask(__name__)

# Конфігурація
API_KEY = 'ваш_api_ключ_openweathermap'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form['city']
        if city:
            try:
                params = {
                    'q': city,
                    'appid': API_KEY,
                    'units': 'metric',
                    'lang': 'ua'
                }
                response = requests.get(BASE_URL, params=params)
                data = response.json()

                if response.status_code == 200:
                    weather_data = {
                        'city': data['name'],
                        'temp': round(data['main']['temp']),
                        'feels_like': round(data['main']['feels_like']),
                        'description': data['weather'][0]['description'].capitalize(),
                        'icon': data['weather'][0]['icon'],
                        'humidity': data['main']['humidity'],
                        'wind': round(data['wind']['speed']),
                        'pressure': round(data['main']['pressure'] * 0.750062),
                        'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                        'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                        'time': datetime.now().strftime('%H:%M, %d.%m.%Y')
                    }
                else:
                    error = f"Місто '{city}' не знайдено. Спробуйте ще раз."
            except Exception as e:
                error = "Сталася помилка при отриманні даних. Спробуйте пізніше."

    return render_template('index.html', weather=weather_data, error=error)


if __name__ == '__main__':
    # Запускаємо Flask-додаток на 0.0.0.0 (доступ з усіх IP)
    port = int(os.environ.get('PORT', 5000))  # Можна змінити через змінну середовища PORT
    app.run(host="0.0.0.0", port=port, debug=False)