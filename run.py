from flask import Flask
from flask import render_template, redirect, request, url_for
import os
from app.processing import composeTimeQueryParameters, composeWeatherAPI, droptailForecast, assignUIMarkers, processWeatherData
from apscheduler.schedulers.background import BackgroundScheduler

config_type = "dev" # "dev" or "prod"

app = Flask(__name__)

configuration = os.path.join(os.getcwd(), "config", config_type+".py")
app.config.from_pyfile(configuration)

type = app.config['TYPE']
place =  app.config['PLACE']
forecast_days = app.config['FORECAST_DAYS_MAX']
interval_hours = app.config['DATA_INTERVAL_HOURS']
parameters = app.config['PARAMETERS']

weatherAPI = composeWeatherAPI(type, place, parameters, forecast_days, interval_hours)

@app.route("/", methods=["GET","POST"])
def index():
    last_forecast, last_timestamp, timestamp = refreshWeatherData()
    return render_template("index.html", forecast=last_forecast, timestamp=last_timestamp, place=place.capitalize())

@app.route("/try_place", methods=["POST", "GET"])
def try_place():
    """
    process user input for weather forecast city
    if accessed not from the button, also causes correct except redirect
    """
    global place, weatherAPI
    try:
        try_place = request.form['place']
        try_weatherAPI = composeWeatherAPI(type, try_place, parameters, forecast_days, interval_hours)
        forecast, timestamp = processWeatherData(try_weatherAPI)
        if forecast:
            place = try_place
            weatherAPI = try_weatherAPI
        return redirect(url_for("index"))
    except:
        # print(f'\nFrom try_place: Except caught, {try_place}, {try_weatherAPI}\n')
        return redirect(url_for("index"))

@app.route("/server", methods=["GET","POST"])
def server():
    return render_template("server.html", timestamp=timestamp, last_timestamp=last_timestamp, type=type, place=place.capitalize())

def refreshWeatherData():
    global timestamp, last_forecast, last_timestamp
    forecast, timestamp = processWeatherData(weatherAPI)
    if forecast:
        last_forecast = forecast
        last_timestamp = timestamp
    return last_forecast, last_timestamp, timestamp

scheduler = BackgroundScheduler()
scheduler.add_job(refreshWeatherData, "interval", minutes=app.config['REQUEST_INTERVAL_MINUTES'])
scheduler.start()

if __name__=="__main__":
    print(f'Weather service started. Using API: {weatherAPI}\n')
    # last_forecast and last_timestamp keep information of last successful connection
    last_forecast, timestamp = processWeatherData(weatherAPI)
    if last_forecast:
        last_timestamp = timestamp
    else:
        last_timestamp = 'None'
    app.run()

scheduler.shutdown()
