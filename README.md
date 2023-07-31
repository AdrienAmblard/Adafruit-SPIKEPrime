# Adafruit-SPIKEPrime
Code used to build a PyScript which creates a connection between an Adafruit IO dashboard and a LEGO SPIKE Prime hub.\
Refer to this [Notion page](https://www.notion.so/LEGO-SPIKE-Prime-Adafruit-Dashboard-8705d4ed60464339a6e0c5e5dffd241f?pvs=4) for full project description.\
\
## Ada.py
The connection between the Pyscript website and the Adafruit IO dashboard occurs through _get_ requests with its REST API. The Ada class contains all the functions need to retrieve or push information to the API. It also contains functions which generalize the parsing of the json data.\
\
## control.py
This file contains a series of functions matches code to the API feeds in order to determine when each code should run. The keystone function in this file is called 'checking()', which runs a loop as long as a corresponding feed on the API is equal to 1. This loop refreshes the values of all the relevant feeds and runs specific code based on their values. 
