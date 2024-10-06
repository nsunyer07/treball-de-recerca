from time import sleep as t
from dades import TdR
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import gpiozero
tdr = TdR(5)
rele1 = gpiozero.OutputDevice(5)
rele2 = gpiozero.OutputDevice(6)
temperatura_min = 14
humitat_min = 40

while True:
    try:
        tdr.enviar_dades()
        var1 = tdr.mostra_temperatura()
        var2 = tdr.mostra_humitat()
        tdr.desconecta
        msg = subscribe.simple("humitat_solTdR2", hostname="broker.emqx.io")
        msg = msg.payload
        msg = msg.decode("utf-8")
        msg = msg.split()
        if msg[0] == "temperatura":
            temperatura_min = msg[1]
        elif msg[0] == "humitat":
            humitat_min = msg[1]
        elif msg == "no canvi":
            humitat_min = humitat_min
            temperatura_min = temperatura_min
        if float(var1) <= temperatura_min:
            rele1.toggle()
            t(30)
            rele1.toggle()
        elif float(var2) <= humitat_min:
            rele2.toggle()
            t(15)
            rele2.toggle()
        t(2)
    except RuntimeError as error:
        print(error.args[0])
        t(2)
        continue
