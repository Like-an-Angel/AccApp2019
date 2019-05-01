*** Settings ***
Documentation     A test suite for inputting invalid forecast places.
Resource          resource.robot

Suite Setup     Open Browser To Weather Forecast Page
Suite Teardown  Close Browser

*** Test Cases ***
Invalid Place Change
    Input Place    Oulu
    Submit Place
    Weather Forecast Page Should Be Open
    City Should Be      Oulu
    Input Place    ÖUiyb
    Submit Place
    Weather Forecast Page Should Be Open
    City Should Be      Oulu
