import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "mwlcx2"
deviceType = "rasberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "78901234"

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        voltage=random.randint(1,5)
        #print(voltage)
        current=random.randint(0,220)
        power=voltage*current
        #Send Temperature & Humidity to IBM Watson
        data = { 'Voltage' : voltage, 'Current': current, 'Power': power}
        #print (data)
        def myOnPublishCallback():
            print ("Published Voltage = %s V" % voltage, "Current= %s Amp" % current, "Power= %s " %power, "to IBM Watson")

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
