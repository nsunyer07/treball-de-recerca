from time import sleep as t
import paho.mqtt.client as mqtt
from gpiozero import LED, MCP3008
import board
import adafruit_dht
s_humitat = MCP3008(0)

def lectura(temps):
    #try:
        temperature_c = adafruit_dht.DHT22(board.D14, use_pulseio=False).temperature
        humidity = adafruit_dht.DHT22(board.D14, use_pulseio=False).humidity
        humitat = round(100-s_humitat.value*100,1)
            
        dades = (f" {temperature_c} {humidity} {humitat} ")
        return(dades)
        t(temps)
    #except RuntimeError as error:
        #print(error.args[0])
        #t(2)
def on_connect(client, userdata, flags, rc):
    print(f"connectat amb codi {rc}")
    client.subscribe("humitat_solTdR1")
    
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
          

def on_publish(client, userdata, mid, reason_code, properties):
    userdata.remove(mid)



class TdR:
    def __init__(self, temps):
        self.temps = temps
    def enviar_dades(self):
        unacked_publish = set()
        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.on_publish = on_publish
        mqttc.user_data_set(unacked_publish)
        mqttc.connect("broker.emqx.io")
        mqttc.loop_start()
        dades = lectura(1)
        msg_info = mqttc.publish("humitat_solTdR1", dades, qos=0)
        unacked_publish.add(msg_info.mid)
        while len(unacked_publish):
            t(0.1)
        msg_info.wait_for_publish()
        self.temps

    def mostra_temperatura(self):
        dades = lectura(1)
        return(float(f"{dades.split()[0]}"))

    def mostra_humitat(self):
        dades = lectura(1)
        return(float(f"{dades.split()[2]}"))
    def desconecta():
        mqtcc.disconnect()
        t(1)

