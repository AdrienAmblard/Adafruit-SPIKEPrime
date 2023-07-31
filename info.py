import js , pyodide
from pyscript import Element

ADA_KEY = ''
ADA_USERNAME = ''
GROUP_NAME = ''
FEED_NAME = ''
Adafruit_pass = {'key':ADA_KEY,'username':ADA_USERNAME}

def retrieve(attribute,name,id):
    val = Element(name).element.value
    attribute = val
    Element(name).element.value = ''
    printedVal = js.document.getElementById(id)
    printedVal.innerHTML = val

def showKeys(): 
    if  js.document.getElementById('square').style.display == 'none':
        js.document.getElementById('square').style.display = 'block'
        js.document.getElementById('keyInputCont').style.display = 'grid inline'
    elif js.document.getElementById('square').style.display == 'block':
        js.document.getElementById('square').style.display = 'none'
        js.document.getElementById('keyInputCont').style.display = 'none'
