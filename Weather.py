from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = ""
    error = None

    if request.method == "POST":
        city = request.form["city"]
        url = f"https://wttr.in/{city}?format=j1"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            current = data["current_condition"][0]
            weather_data = {
                "місто": city.title(),
                "температура": current["temp_C"],
                "відчувається_як": current["FeelsLikeC"],
                "опис": current["weatherDesc"][0]["value"],
                "вологість": current["humidity"],
                "вітер": current["windspeedKmph"]
            }
        except Exception:
            error = "Ой, щось пішло не так. Перевір назву міста."

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
