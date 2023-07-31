import requests, json , pyodide_http ,asyncio
from info import *
pyodide_http.patch_all()

class Ada():
    def __init__(self):
        self.key = Adafruit_pass['key']
        self.user = Adafruit_pass['username']
        self.headers = {'X-AIO-Key':self.key,'Content-Type':'application/json'}
        self.keys = []
        self.feeds = []
        self.groups = []
        self.names = []
        self.values = []
        
    def GetList(self):
        url = 'https://io.adafruit.com/api/v2/%s/feeds' % self.user
        reply = requests.get(url,headers=self.headers)
        if reply.status_code == 200:
            reply = json.loads(reply.text)
            self.keys = [x['key'] for x in reply]
            self.groups = [x['group']['name'] for x in reply]
            self.names = [x['name'] for x in reply]
            self.values = [x['last_value'] for x in reply]
            self.ids = [x['id'] for x in reply]
            return True
        return False
    
    def Update(self, group = 'LEGO Spike Prime', names = 'Motor State', values = [0]):
        indices = [i for i, x in enumerate(self.groups) if x == group]
        if len(values) != len(indices):
            print('mismatch in number of values for group %s' % group)
            print(len(values),len(indices))
            print([self.keys[i] for i in indices])
            return
        
        for i,index in enumerate(indices):
            if names[i] in self.names:
                self.Save(group, names[i], values[i])
            else:
                print(names[i] + ' is not in ',end='')
                print(self.names)
        return

    def Valid(self, group = 'LEGO Spike Prime', feed = 'Motor State'):
        if group not in self.groups:
            print('group not declared')
            return None
        if feed not in self.names:
            print('feed %s not part of group %s' % (feed, group))
            return None
        index = self.names.index(feed)
        url = 'https://io.adafruit.com/api/v2/%s/feeds/%s/data' % (self.user, self.keys[index])
        return url

    def Get(self, group = 'LEGO Spike Prime', feed = 'Motor State'):
        validURL = self.Valid(group, feed)
        if not validURL:
            return None
        reply = requests.get(validURL+'/last',headers=self.headers)
        return json.loads(reply.text)['value']

    def Save(self, group = 'LEGO Spike Prime', feed = 'Force sensor', value = 0):
        validURL = self.Valid(group, feed)
        if not validURL:
            return None
        data = {'value':value}
        reply = requests.post(validURL,headers=self.headers,json=data)
        if reply.status_code != 200:
            print('Error %d: %s' % (reply.status_code, reply.text))
            return False
        return reply
			
