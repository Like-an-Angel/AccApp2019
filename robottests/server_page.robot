*** Settings ***
Documentation     A test suite for checking server page displaying a correct place.
Resource          resource.robot

Suite Setup     Open Browser To Weather Forecast Page
Suite Teardown  Close Browser

*** Test Cases ***
Valid Server Page Place
    Input Place    Mikkeli
    Submit Place
    Weather Forecast Page Should Be Open
    Go To Server Page
    Server Page Should Be Open
    Server Should Show City      Mikkeli
