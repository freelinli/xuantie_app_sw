from mqttlink import MqttLink

class MqttServer(MqttLink):
    def device_sub_process(self, payload):
        print("MqttServer device_sub_process")

if __name__ == "__main__":
    mqtt_server = MqttServer(mode = "sub", topic = "link",  clientid = "ServerA")
    mqtt_server.device_disconnect()