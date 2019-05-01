# AccApp2019

Weather forecast application. Displays a forecast for up to a week for a place (city) in Finland, which can be modified by user.
City and other parameters can be modified from configuration files in folder "config", however not any parameters can produce valid or non-empty results. More info on: https://en.ilmatieteenlaitos.fi/open-data

Forecast service is accessed from http://localhost:5000/ and is updated when user visits the home page or after changing the forecast city as well as by scheduler. Time between scheduled requests can be adjusted in config file by modifying REQUEST_INTERVAL_MINUTES value, which should be integer.
If request is not successful, last received non-empty forecast is displayed.

Server page http://localhost:5000/server shows current monitored city and the status of updates, with timestamps of last received forecast data as well as last connection attempt.

Installation guide:

Clone this repository to a local folder with command "git clone https://github.com/Like-an-Angel/AccApp2019.git"

For environment and package management, Pipenv is used.
To prepare the environment, after Pipenv is installed, from the project folder run "pipenv install --dev" to install the dependencies specified in Pipfile.lock including packages needed for running unit and robot tests.
Alternatively, command "pipenv install" installs only packages needed for executing the application.

To activate the environment, run "pipenv shell"
Now, application can be started by command "python run.py" and accessed from http://localhost:5000/

Project includes unit tests and robot tests.
To run all unit tests, from project folder run command "python -m unittest discover"
To run robot tests, start the app and from robottests folder run test case files by command "robot testcase.robot", each of which generates report.html and log.html files with detailed results.

API used by default is: fmi::forecast::harmonie::surface::point::simple
Alternatively fmi::forecast::hirlam::surface::point::simple can be set in configuration.
Example: http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::harmonie::surface::point::simple&place=helsinki&parameters=Temperature,Humidity,WindSpeedMS&timestep=360
