from datetime import datetime, timedelta
import arrow, calendar
from app.weatherService import fetchWeatherData

timezone = 'GMT+3'
precipitationAmountThreshold = 0.0
windSpeedMSThreshold = 3.0
temperatueThreshold = 0.0
dayThreshold = 7.0
nightThreshold = 20.0

def composeTimeQueryParameters(days = 7, hours = 6):
    startday = datetime.now()
    endday = startday + timedelta(days=days)

    starttime = startday.isoformat().split('T')[0] + 'T00:00:00Z'
    endtime = endday.isoformat().split('T')[0] + 'T00:00:00Z'

    timestep = hours * 60

    return starttime, endtime, timestep

def composeWeatherAPI(type, place, parameters, forecast_days, interval_hours):
    starttime, endtime, timestep = composeTimeQueryParameters(forecast_days, interval_hours)

    weatherAPI = f'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id={type}&place={place}&parameters={parameters}&starttime={starttime}&endtime={endtime}&timestep={timestep}'

    return weatherAPI

def droptailForecast(forecast):
    """
    remove empty records for dates with unavailable forecast
    """
    for record in sorted(forecast.keys(), reverse=True):
        # forecast[record].values() is a dict of all parameters for the timestamp 'record'
        if 'NaN' in forecast[record].values():
            del forecast[record]
        # else:
        #     return forecast
    return forecast

def assignUIMarkers(forecast):
    """
    add to forecast dictionary fields for frontend
    """
    # raw api timestamps are in zulu time
    for zulutime in forecast.keys():
        local_datetime = str(arrow.get(zulutime).to(timezone))
        # print(f"Arrow time: {local_datetime}")
        # Humanizing the date to format: DD of MON
        date_split = local_datetime.split('T')[0].split('-')
        forecast[zulutime]['date'] = f'{date_split[2]} of {calendar.month_abbr[int(date_split[1])]}'

        hours = local_datetime.split('T')[1].split(':')[0]
        forecast[zulutime]['hours'] = hours + ':00'

        # Forming an icon code corresponding to amount of rain and wind speed for days and nights
        if float(forecast[zulutime]['PrecipitationAmount']) > precipitationAmountThreshold:
            precipitation = 'r' # rainy
        else:
            precipitation = 'd' # dry
        if float(forecast[zulutime]['WindSpeedMS']) > windSpeedMSThreshold:
            wind = 'w' # windy
        else:
            wind = 's' # still
        if dayThreshold < float(hours) < nightThreshold:
            light = 'd' # day
        else:
            light = 'n' # night

        forecast[zulutime]['icon'] = light + precipitation + wind + '-icon'

        # Lower and higher temperatures get different color in termometer visualization
        forecast[zulutime]['Temperature'] = float(forecast[zulutime]['Temperature'])
        if forecast[zulutime]['Temperature'] >= temperatueThreshold:
            forecast[zulutime]['temperature-color'] = 'temperature-warm'
        else:
            forecast[zulutime]['temperature-color'] = 'temperature-cold'

    return forecast

def processWeatherData(weatherAPI):
    """
    forecast update routine
    """
    forecast, timestamp = fetchWeatherData(weatherAPI)
    # print(f'Processing: After fetch: {forecast}\n')
    forecast = droptailForecast(forecast)
    # print(f'Processing: After droptail: {forecast}\n')
    forecast = assignUIMarkers(forecast)

    return forecast, timestamp
