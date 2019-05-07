import requests
import xmltodict
from datetime import datetime

def fetchWeatherData(apiRequest):
    forecast = dict()
    timestamp = datetime.now().isoformat().split('.')[0]
    print(f"Call fetchWeatherData at {timestamp} local time\n")
    try:
        data = requests.get(apiRequest).content
    except:
        print(f'Errors while fetching weather data')
        return dict(), timestamp

    data = xmltodict.parse(data)['wfs:FeatureCollection']
    # timestamp = data['@timeStamp']
    data = data['wfs:member'] # an array; a separate 'member' for each parameter entry

    for member in data:
        record = member['BsWfs:BsWfsElement']
        # For each unique datetime form own dictionary of all existing parameters
        if record['BsWfs:Time'] not in forecast:
            forecast[record['BsWfs:Time']] = dict()
        forecast[record['BsWfs:Time']][record['BsWfs:ParameterName']] = record['BsWfs:ParameterValue']

    # print(f'From fetchWeatherData>forecast: {forecast}\n')

    return forecast, timestamp
