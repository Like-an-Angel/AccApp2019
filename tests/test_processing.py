# pytest package
# simple unittests. To run, from the project folder: python -m unittest discover

import unittest
from app.processing import composeTimeQueryParameters, droptailForecast, assignUIMarkers
import os
from datetime import datetime, timedelta
import arrow


class TestComposeTimeQueryParameters(unittest.TestCase):

    def test_composeTimeQueryParameters(self):
        # check returning data types
        self.starttime, self.endtime, self.timestep = composeTimeQueryParameters(days = 7, hours = 6)
        assert isinstance(self.starttime, str)
        assert isinstance(self.endtime, str)
        assert isinstance(self.timestep, int)

        # iso dates YYYY-MM-DD +T
        self.assertEqual(len(self.starttime.split('T')[0].split('-')), 3)
        self.assertEqual(len(self.starttime.split('T')[0].split('-')), 3)

        # check day difference
        self.assertEqual(datetime.fromisoformat(self.starttime.split('Z')[0]) + timedelta(days=7), datetime.fromisoformat(self.endtime.split('Z')[0]))

        self.assertEqual(self.timestep, 6*60)

class TestDroptailForecast(unittest.TestCase):

    def test_droptailForecast(self):
        # Nothing to drop
        mock_forecast = {'1':{'a':1, 'b':1, 'c':1}, '2':{'a':1, 'b':1, 'c':1}, '3':{'a':1, 'b':1, 'c':1}, '4':{'a':1, 'b':1, 'c':1}}
        self.assertEqual(sorted(droptailForecast(mock_forecast).keys()), ['1','2','3','4'])

        # 2 records to drop, the latter has one NaN element, the former all NaN elements
        mock_forecast = {'1':{'a':1, 'b':1, 'c':1}, '2':{'a':1, 'b':1, 'c':1}, '3':{'a':'NaN', 'b':'NaN', 'c':'NaN'}, '4':{'a':'NaN', 'b':1, 'c':1}}
        self.assertEqual(sorted(droptailForecast(mock_forecast).keys()), ['1','2'])

        # All records have NaN elements
        mock_forecast = {'1':{'a':1, 'b':1, 'c':'NaN'}, '2':{'a':1, 'b':'NaN', 'c':1}, '3':{'a':'NaN', 'b':'NaN', 'c':'NaN'}, '4':{'a':'NaN', 'b':1, 'c':1}}
        self.assertEqual(sorted(droptailForecast(mock_forecast).keys()), [])

class TestAssignUIMarkers(unittest.TestCase):

    def test_assignUIMarkers(self):
        """
        Reference parameters @01.05.2019
        timezone = 'GMT+3'
        precipitationAmountThreshold = 0.0
        windSpeedMSThreshold = 3.0
        temperatueThreshold = 0.0
        dayThreshold = 7.0
        nightThreshold = 20.0
        """

        mock_forecast = {'1111-01-01T09:00:00Z':{'PrecipitationAmount':'1.0', 'WindSpeedMS':'0', 'Temperature':'1'}, '2222-02-02T09:00:00Z':{'PrecipitationAmount':'0.0', 'WindSpeedMS':'5.0', 'Temperature':'1'}, '3333-03-03T09:00:00Z':{'PrecipitationAmount':'1.0', 'WindSpeedMS':'0', 'Temperature':'-1'}, '4444-04-04T23:00:00Z':{'PrecipitationAmount':'5.0', 'WindSpeedMS':'0', 'Temperature':'1'}}
        test_forecast = assignUIMarkers(mock_forecast)

        self.assertEqual(test_forecast['1111-01-01T09:00:00Z']['date'], '01 of Jan')
        self.assertEqual(test_forecast['2222-02-02T09:00:00Z']['hours'], '12:00') # Only for GMT+3

        self.assertEqual(test_forecast['2222-02-02T09:00:00Z']['temperature-color'], 'temperature-warm')
        self.assertEqual(test_forecast['3333-03-03T09:00:00Z']['temperature-color'], 'temperature-cold')

        self.assertEqual(test_forecast['2222-02-02T09:00:00Z']['icon'], 'ddw-icon') # day-dry-windy
        self.assertEqual(test_forecast['4444-04-04T23:00:00Z']['icon'], 'nrs-icon') # night-rainy-still
