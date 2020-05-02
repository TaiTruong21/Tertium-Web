import requests
import time
from jetbot import Robot

print("hello")

myJetBot = Robot()

URL = "http://192.168.43.225:5001"
currMoveId = 0

while True:
    r = requests.get(url = (URL+"/moves/next"))
    
    if r.content.decode("utf-8")!="\"Null\"":
        if not currMoveId==0:
            requests.get(url=(URL+"/moves/fin/"+str(currMoveId)))

        print(r.json())
        jsn=r.json()
        print(type(jsn))
        currMoveId = jsn['moveId']
        
        if jsn['direction']=="forward":
            myJetBot.forward(0.1)
        if jsn['direction']=="backward":
            myJetBot.backward(0.1)
        if jsn['direction']=="left":
            myJetBot.left(0.1)
        if jsn['direction']=="right":
            myJetBot.right(0.1)
        if jsn['direction']=="stop":
            myJetBot.stop()
        
            
        
    else:
        print("No further command..")
    
    time.sleep(3)