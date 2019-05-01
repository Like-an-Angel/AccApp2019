*** Settings ***
Documentation     Keywords and variables list for AccApp2019
Library           SeleniumLibrary
Library           Process

*** Variables ***
${APPLICATION}      http://localhost:5000
${BROWSER}          Chrome
${DELAY}            0
${HOME URL}         ${APPLICATION}/
${SERVER URL}       ${APPLICATION}/server
${APPRUN}           python run.py
${APP}=             Run python run.py

*** Keywords ***
Open Browser To Weather Forecast Page
    Open Browser    ${HOME URL}     browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Weather Forecast Page Should Be Open

Weather Forecast Page Should Be Open
    Title Should Be    Weather Forecast

Go To Server Page
    Go To    ${SERVER URL}
    Weather Forecast Page Should Be Open

Input Place
    [Arguments]    ${place}
    Input Text    place    ${place}

Submit Place
    Click Button    place-button

Server Page Should Be Open
    Location Should Be    ${SERVER URL}
    Title Should Be    Weather Forecast

City Should Be
    [Arguments]     ${place}
    Textfield Value Should Be    place       ${place}

Server Should Show City
    [Arguments]     ${place}
    ${city}=        Get Text        place
    Should Be Equal     ${city}     ${place}
