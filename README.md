# Adafruit - SPIKE Prime
Code used to build a PyScript which creates a connection between an Adafruit IO dashboard and a LEGO SPIKE Prime hub.\
Refer to this [Notion page](https://www.notion.so/LEGO-SPIKE-Prime-Adafruit-Dashboard-8705d4ed60464339a6e0c5e5dffd241f?pvs=4) for full project description.\
**Note**: _The code in this repository is for a system whose dashboard only has a toggle switch on it, and two possible scripts can be run (ON or OFF). It should can be changed accordingly to accomodate for more complex dashboards._

## Ada.py
The connection between the Pyscript website and the Adafruit IO dashboard occurs through _get_ requests with its REST API. The _Ada_ class contains all the functions need to retrieve or push information to the API. It also contains functions which generalize the parsing of the json data.

## control.py
This file contains a series of functions matches code to the API feeds in order to determine when each code should run. The keystone function in this file is called 'checking()', which runs a loop as long as a corresponding feed on the API is equal to 1. This loop refreshes the values of all the relevant feeds and runs specific code based on their values. 

## info.py
The connection to the Adafruit REST API depends of having access to the user's API Key and Adafruit username. Furthermore, the generalized parsing in Ada.py depends on group name to find certain information -- in this case I have also included the feed name to simplify the setup. This file contains the functions needed to retrieve each of these fields from the inputs on the webpage. 

## serial.py
The _serial_ class contains all of the functions needed to open a serial port from the PyScript website and connect to LEGO SPIKE Prime hub. A key feature of this class is the creation of a REPL which displays the code which is being run on the SPIKE Prime hub and what it returns. This includes a variable called 'last_line' which holds the last line in the REPL to extract sensor values. 
