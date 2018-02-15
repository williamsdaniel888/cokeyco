import logging
import threading
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import datetime
import json
import paho.mqtt.client as mqtt
#setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


MQTTServer = "localhost"



class MQTT(threading.Thread):
    def __init__(self,eventMap):
        threading.Thread.__init__(self)
        logging.info("Started MQTT thread")
        self.eventMap = eventMap
        self.killThread = threading.Event()

    def decodeEvent(self,msg):
        if msg in self.eventMap.keys():
            logger.info("Event %s recieved and emmitted",msg)
            self.eventMap[msg].set()
        else:
            logger.error("Did not recognise event: %s  :when decoding",msg)


    def music_message(self,mosq, obj, msg):
        #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        message = msg.payload.decode("utf-8") 
        
        if message =="PIR":
            j = json.dumps({"PIR":str(datetime.datetime.now()) })
            self.myAWSIoTMQTTClient.publish("ShowerMate/PIR", bytes(j,"utf-8"), 1)
            logger.info('Sent PIR to AWS: ShowerMate/PIR')


        if message == "play" or message=="pause" or message == "next" or message == "previous":
            self.decodeEvent(message)
        else:
            logger.warn("MQTT message not recognised, message: %s",message)

    def AWSCallback(self,client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")


    def run(self):
        logging.info("Setting up MQTT subscribe")

        music_client = mqtt.Client("music_Stream")
        music_client.connect(MQTTServer)
        music_client.subscribe("musicControl")
        music_client.subscribe("showerMate/PIR")
        music_client.on_message = self.music_message
        logger.info("Started listeing to musi cMessages on %s",MQTTServer)
        while not self.killThread.is_set():
            #poll for events, blocks with time of 0.1s
            music_client.loop(0.1)
        logger.info("Kill thread Recieved, thread %s is shutting down", __name__)

        #AWS Secrets
        host = ""
        rootCAPath = ""
        certificatePath = ""
        privateKeyPath = ""
        clientId = "MyClient"
        topic = "ShowerMate/Commands"



        # Init AWSIoTMQTTClient
        self.myAWSIoTMQTTClient = None
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        self.myAWSIoTMQTTClient.configureEndpoint(host, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)


        # AWSIoTMQTTClient connection configuration
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        self.myAWSIoTMQTTClient.subscribe(topic, 1, self.AWSCallback)