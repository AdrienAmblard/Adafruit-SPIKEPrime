import asyncio , serial , info 
from Ada import *


async def sendCode(code):
# sends code to Spike Prime and runs it 
    await serial.s.upload(code)
    
async def wait_for_time(seconds):
# replacement for time.sleep() which is not supported in pyscript
	await asyncio.sleep(seconds)

async def checking():
# checks if the checking switch on the dashboard is on
# if checking is on, a while loop opens and the values of the API are refreshed

    # this prevents user from checking if Spike Prime is not connected 
    statusImg = js.document.getElementById("SPImg")
    #if statusImg.src != 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Ski_trail_rating_symbol-green_circle.svg/1200px-Ski_trail_rating_symbol-green_circle.svg.png':
     #   js.alert('Connect the Spike Prime')
      #  return

    # codes used in sendCode() are extracted from REPLs so user can define them from main page 
    code1 = serial.REPL_Read('py-repl1')
    code2 = serial.REPL_Read('py-repl2')
    ran = 0
    aio = Ada()
    aio.GetList()
    check = aio.Get(GROUP_NAME,'Checking')
    dashImg = js.document.getElementById('DashImg')
    buttonImg = js.document.getElementById('ButtonImg')
    lastlineSpan = js.document.getElementById('lastline')
    
    if check == '0':
        print('Dashboard is deactivated')
        dashImg.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Red_X.svg/1200px-Red_X.svg.png"
        return
    else: 
        print('Awaiting input...')
        
        # while loop runs as long as the checking button is on 
        # refreshes values from the API every iteration (2s delay)
        # if the button is on it sends code1 and code 2 if it is off 
        while check == '1':
            dashImg.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Ski_trail_rating_symbol-green_circle.svg/1200px-Ski_trail_rating_symbol-green_circle.svg.png"
            check  = aio.Get(GROUP_NAME,'Checking')
            value = aio.Get(GROUP_NAME,FEED_NAME)
            print(value)
            if ran == 0:
                if value == '1':
                    await sendCode(code1)
                    ran = 1
                    buttonImg.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Ski_trail_rating_symbol-green_circle.svg/1200px-Ski_trail_rating_symbol-green_circle.svg.png"
                else:
                    await sendCode(code2)
                    buttonImg.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Red_X.svg/1200px-Red_X.svg.png"
            '''        
            try:
                int(serial.last_line)
            except:
                await wait_for_time(2)
                lastlineSpan.innerHTML = serial.last_line
                continue
            aio.Save(GROUP_NAME,"Force sensor",serial.last_line)
            '''
            lastlineSpan.innerHTML = serial.last_line
            await wait_for_time(2)
        print('Dashboard is deactivated')
        dashImg.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Red_X.svg/1200px-Red_X.svg.png"
        

async def getForce():
    code = '''import force_sensor
from hub import port
force_sensor.force(port.E)'''  
    await serial.s.upload(code)

def pushGraph():
    aio.Save(GROUP_NAME,"Force sensor",last_line)
