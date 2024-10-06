import streamlit as st
import pandas as pd
import time
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
st.cache_resource()
# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Control Domòtic',
    page_icon=':seedling:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.
def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
        userdata.remove(mid)
unacked_publish = set()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish
def on_message(client, userdata, message):
    pass
mqttc.user_data_set(unacked_publish)
mqttc.connect("broker.emqx.io")
mqttc.loop_start()

def canvitemp():
    msg_info = mqttc.publish("humitat_solTdR2", f"temperatura {st.session_state.temp}", qos=0)
    unacked_publish.add(msg_info.mid)
    msg_info.wait_for_publish()
def canvihumi():
    msg2_info = mqttc.publish("humitat_solTdR2", f"humitat {st.session_state.humi}", qos=0)
    unacked_publish.add(msg2_info.mid)
    msg2_info.wait_for_publish()
def nocanvi():
    msg3_info = mqttc.publish("humitat_solTdR2", "no canvi", qos=0)
    unacked_publish.add(msg3_info.mid)
    msg3_info.wait_for_publish()
# Crear un título
st.title('Control Domòtic')

# Cargar datos

temp_min =25
hum_min = 40
st.write("""Aquests sliders serveixen per cambiar 
         la temperatura i la humitat minima del sistema.
""")
st.slider("Humitat del sól", min_value=0, max_value=100, value= 40, step=None, format=None, key="humi", help=None, on_change=canvihumi, args=None, kwargs=None, disabled=False, label_visibility="visible")
st.slider("Temperatura", min_value=0, max_value=40, value= 14, step=None, format=None, key="temp", help=None, on_change=canvitemp, args=None, kwargs=None, disabled=False, label_visibility="visible")
st.write("""Aquestes son les dades de temperatura i humitat 
         recollides de més nova a més vella anant d'esquerra a dreta.
         """)
label = ["temperatura", "humitat", "humitat_sol"]
datos = pd.DataFrame( index = [])
placeholder = st.empty()
placeholder2 =st.empty()
# Crear un slider


try:
    while True:
        nocanvi()
        msg = subscribe.simple("humitat_solTdR1", hostname="broker.emqx.io")
        #if time.time()
        msg = msg.payload
        msg = msg.decode("utf-8")
        msg = msg.split()
        # Añadir nuevos datos a los datos existentes
        datos2 = pd.DataFrame(msg, index=[label])
        datos = pd.concat( objs= (datos2, datos), axis=1,  ignore_index=True)
        nocanvi()
        with placeholder.container():
            st.write(datos)
        with placeholder2.container():
            st.write(f'Temperatura actual: {msg[0]}Cº')
            st.write(f'Humitat ambiental actual: {msg[1]}%')
            st.write(f'Humitat del sòl actual: {msg[2]}%')
        time.sleep(2)
except RuntimeError as error:
    st.write(error.args[0])
    time.sleep(5)
