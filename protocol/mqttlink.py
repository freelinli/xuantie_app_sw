import sys
import paho.mqtt.client as mqtt

class MqttLink:
    def __init__(self, mode, topic = "test", clientid = "66666666", qos = 0, ip = '192.168.10.51', port = 1883, keepalivetime = 10):
        self.mode = mode
        self.topic =  topic
        self.qos = qos
        self.ip = ip
        self.port = port
        self.keepalivetime = keepalivetime
        self.clientid = clientid
        print("mode: " ,  mode)
        def mqtt_connect(client, userdata, flags, rc):
            print("Connected with result code: " + str(rc))

        def mqtt_message(client, userdata, msg):
            print("mqtt_message ------------------------------")
            print("the length of payload is :", len(msg.payload))
            print("topic :" + msg.topic + " " + str(msg.payload))
            for c in msg.payload:
                print("int %03d: hex 0x%02x: char [%c]" % (c, c, c))
            print("mqtt_message ------------------------------ end ")
            self.device_sub_process(msg.payload)
        def mqtt_disconnect(client, userdata, rc):
            if rc != 0:
                print("Unexpected disconnection %s" % rc)
            else:
                print("successful disconnection %s" % rc)
        self.client = mqtt.Client(self.clientid)
        self.client.on_connect = mqtt_connect
        self.client.on_message = mqtt_message
        self.client.on_disconnect = mqtt_disconnect
        if (self.mode == "sub"):
            self.client.will_set("clientstatus", str({ "LOST_CONNECTION": self.clientid, "mode": "sub"}), 0, False)
            self.client.connect(self.ip, self.port, self.keepalivetime)
            self.client.subscribe(self.topic, self.qos)
            print("sub loop_forever ------------------------------")
            self.client.loop_forever()
        elif (self.mode == "pub"):
            self.client.will_set("clientstatus",str({ "LOST_CONNECTION": self.clientid, "mode": "pub"}), 0, False)
            self.client.connect(self.ip, self.port, self.keepalivetime)
        else :
            print("self mode should be sub or pub")
    def mqtt_send(self, content = [0x00, 0x02, 0x66, 0x66, 0x66, 0x66, 0x80, 0x01, 0x01, 0x12, 0x1c]):
        byteArr = bytearray(content)
        print(byteArr)
        self.client.publish(self.topic, payload = byteArr, qos = self.qos)

    def device_sub_process(slef, payload):
        print("mqtt_common device_sub_process")

    def device_disconnect(self):
        if (self.mode == "sub"):
            self.client.publish("clientstatus", str({ "LOST_CONNECTION": self.clientid, "mode": "sub"}))
        elif (self.mode == "pub"):
            self.client.publish("clientstatus", str({ "LOST_CONNECTION": self.clientid, "mode": "pub"}))
        self.client.disconnect()
        print("mqtt_common disconnect")

class MqttClient(MqttLink):
    def device_sub_process(self, payload):
        print("MqttClient device_sub_process")
    
if __name__ == "__main__":
    mqtt_client = MqttClient(mode = "pub", topic = "link",  clientid = "clientA")
    
    argc = len(sys.argv)
    if (argc > 1):
        print(sys.argv[1])
        mqtt_client.mqtt_send(bytes(sys.argv[1], encoding='utf8'))
        mqtt_client.device_disconnect()
    else:
        print("argc is equal to 1")
        mqtt_client.mqtt_send()
        mqtt_client.device_disconnect()