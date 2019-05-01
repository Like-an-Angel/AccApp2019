*** Settings ***
Documentation     A test suite for changing valid forecast places.
Resource          resource.robot

Suite Setup     Open Browser To Weather Forecast Page
Suite Teardown  Close Browser

*** Test Cases ***
Valid Place Change/Refresh
    Input Place    Pori
    Submit Place
    Weather Forecast Page Should Be Open
    City Should Be      Pori

Valid Secondary Place Change With Finnish Characters
    Input Place    Hämeenlinna
    Submit Place
    Weather Forecast Page Should Be Open
    City Should Be      Hämeenlinna
