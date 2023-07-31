import js ,time , asyncio
from js import navigator
from pyodide.ffi import to_js, create_proxy
from pyscript import Element

last_line = ''
#Utility function for converting py dicts to JS objects
def j(obj):
    return to_js(obj, dict_converter=js.Object.fromEntries)

modifier = ''
ModLUT = {'Shift':'Shift', 'Control':'Control', 'Meta':'Command', 'Alt':'Option'}
KeyLUT = {'Enter':'\r\n', 'Backspace':'', 'ArrowUp':'\x1B[A', 'ArrowDown':'\x1B[B', 'ArrowRight':'\x1B[C', 'ArrowLeft':'\x1B[D', 'Escape':'\t','Backspace':'\b'}
     
def keyDOWN(e):
    global modifier
    payload = e.key
    if payload in ModLUT:
        modifier = ModLUT[payload] 

def keyUP(e):    
    global modifier
    data = e.key 
    payload = ''
    if data in ModLUT:
        modifier = ''  # lifted up the key 
    elif data in KeyLUT:
        payload = KeyLUT[data] 
    else:
        if modifier in ['Command','Control']:
            ctrl = ord(data)-96
            payload = chr(ctrl if ctrl > 0 else ctrl + 32)
        else:
            payload = data
    s.write(payload)

def REPL_Read(repl):
    REPLselected = js.document.getElementById(repl)
    myREPL = REPLselected.querySelectorAll('py-repl .cm-line')
    output = [str(text.textContent)+"\r\n" for text in myREPL]
    return ''.join(output)

async def connect(s):
    await s.ask()
    asyncio.create_task(s.startReading())
    s.CtrlC()
    
class serialCntrl():
    def __init__(self,ref):
        self.connected = False
        self.buffer = ''
        self.buffer2 = ''
        self.consoleText = ''
        self.waiting = 0
        self.cursor = 0
        self.done = False
        self.ref = ref
        if not hasattr(navigator, 'serial'):
            warning = "Use Chrome"
            print(warning)
            raise NotImplementedError(warning)
    
    def VT100(self, text):
        #dt = [ord(text[i]) for i in range(len(text))]
        skip = 0
        for i, char in enumerate(text):
            if skip > 0:
                skip -= 1
                continue
            value = ord(char)
            
            if (value in [9,10,13])|(32<=value<=126): # lower/uppercase letters and symbols
                if self.cursor < len(self.consoleText): #they are using arrow keys to move back/forward
                    self.consoleText = self.consoleText[:self.cursor] + char + self.consoleText[self.cursor+1:]
                else:
                    self.consoleText += char
                
                if value == 10: 
                    self.lastline = self.buffer2 
                    self.buffer2 = '' 
                else: 
                    self.buffer2 += char
                
                self.cursor += 1
            elif (value == 8): #\b - backspace
                self.cursor -= 1
            elif (value in [0,]): #Do nothing with these
                pass
            elif (value == 27): #escape sequence
                skip = 2
                cmd = ord(text[i+2])
                if cmd == 75: #delete to the end
                    self.consoleText = self.consoleText[:self.cursor] 
                else:
                    print('did not recognize ESC: %d' % cmd)
            else:
                print('did not recognize: %d' % value)
        return self.consoleText ,self.lastline
        
    def cprint(self, text):
        global last_line
        [self.consoleText , last_line] = self.VT100(text)
        Element(self.ref).element.innerText = self.consoleText

    async def ask(self):
        self.port = await navigator.serial.requestPort()
        await self.port.open(j({"baudRate": 115200}))
        #self.cprint('Opened Port'+str(self.port))
        self.connected = True
        if self.connected == True:
            statusImg = js.document.getElementById("SPImg")
            statusImg.src = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Ski_trail_rating_symbol-green_circle.svg/1200px-Ski_trail_rating_symbol-green_circle.svg.png"
        else:
            statusImg.src = "https://w7.pngwing.com/pngs/258/656/png-transparent-delete-remove-cross-red-cancel-abort-error-red-cross.png"

            
        # Set up encoder to write to port
        self.encoder = js.TextEncoderStream.new()
        outputDone = self.encoder.readable.pipeTo(self.port.writable)
        # Set up listening for incoming bytes
        self.decoder = js.TextDecoderStream.new()
        inputDone = self.port.readable.pipeTo(self.decoder.writable)
        self.reader = self.decoder.readable.getReader();

    async def startReading(self):
        while not self.done:
            response = await self.reader.read()
            value, done = response.value, response.done
            js.console.log("Read %d: %s" %(len(value),value.encode()))
            self.cprint(value)
            if done:
                break
        self.reader.releaseLock()
        js.console.log("done")

    def write(self, data):
        '''Write to the serial port'''
        if data != '':
            outputWriter = self.encoder.writable.getWriter()
            outputWriter.write(data)
            outputWriter.releaseLock()
            js.console.log(f"Wrote: {data.encode()}")

    def send(self, data):
        self.write(data + '\r\n')

    def read(self, size=1, timeout=1):
        start = time.time()
        spos = len(self.consoleText)
        while (spos + size > len(self.consoleText)) and (time.time() > (start + timeout)):
            pass
        return self.consoleText[spos:]

    def CtrlC(self):
        if self.connected:
            self.send('\x03')
        else:
            print('no connection')

    async def upload(self, value):
        if self.connected:
            value = value.replace('\n','\r\n')
            self.write('\x05' + value + '\x04')
        else:
            print('no connection')

s = None 
def SerialConsole(ref):
    global s
    s = serialCntrl(ref)
    typing = js.document.querySelector('#'+ ref)
    typing.addEventListener('keydown', create_proxy(keyDOWN))
    typing.addEventListener('keyup', create_proxy(keyUP))
