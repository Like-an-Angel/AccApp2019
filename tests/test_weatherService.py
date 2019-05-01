# pytest package
# simple unittests. To run, from the project folder: python -m unittest discover

import unittest
from app.weatherService import fetchWeatherData
import os
import mock

MOCK_API = f"{os.getcwd()}\\tests\\mock-wfs.xml"
"""
Since "requests.get()" can not open local file (for mock API purposes), function is substituted by "mock_requests_get()"
"requests.get()" returns an object and data is accessed by object.content, mockUrlData imitates this object.
"""

class mockUrlData():
    def __init__(self, data):
        self.content = data

def mock_requests_get(path):
    # print(f'I am in mock func, path: {path}')
    file = open(path)
    data = file.read()
    file.close()
    mockData = mockUrlData(data)
    return mockData

class TestFetchWeatherData(unittest.TestCase):
    
    @mock.patch('requests.get', side_effect=mock_requests_get)
    def test_fetchWeatherData_Datatypes(self, mock):
        self.forecast, self.timestamp = fetchWeatherData(MOCK_API)
        assert isinstance(self.forecast, dict)
        assert isinstance(self.timestamp, str)
        self.assertTrue(list(self.forecast.keys())) # mock data is not empty

        first = list(self.forecast.keys())[0]
        assert isinstance(self.forecast[first], dict)
        assert isinstance(self.forecast[first]['Temperature'], str)
        assert isinstance(self.forecast[first]['PrecipitationAmount'], str)
        assert isinstance(self.forecast[first]['WindSpeedMS'], str)

# if __name__=="__main__":
#     unittest.main()
