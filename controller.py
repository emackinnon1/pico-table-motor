import time
from machine import Pin
import network
from umqtt.simple import MQTTClient

# consts
led = machine.Pin("LED", machine.Pin.OUT)
in1 = machine.Pin(0, machine.Pin.OUT)
in2 = machine.Pin(1, machine.Pin.OUT)
button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

# global vars
wlan_cnnct_attempts = 0
table_state = ""
offline = False

# connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("{NETWORK_NAME}", "{PASSWORD}")

while not wlan.isconnected():
    print("Connecting...")
    time.sleep(.5)
    wlan_cnnct_attempts = wlan_cnnct_attempts + 1
    if wlan_cnnct_attempts >= 3:
        offline = True
        
print("Connected!")
# mqtt vars
mqtt_server = '{MQTT_SERVER}'
mqtt_user = '{MQTT_USER}'
mqtt_password = '{MQTT_PASSWORD}'
client_id = 'table_motor_switch'
sub_topic = 'cmd/table_motor_switch'
pub_topic = 'state/table_motor_switch'
PING_INTERVAL = 60
mqtt_con_flag = False
pingresp_rcv_flag = True
lock = True
next_ping_time = 0

# connect to mqtt
mqtt_client = MQTTClient(
    client_id=client_id,
    server=mqtt_server,
    user=mqtt_user,
    password=mqtt_password,
    keepalive=3600
)

def drive_motor(state):
    if state == 'OPEN':
        in1.high()
        in2.low()
    if state == 'CLOSED':
        in1.low()
        in2.high()

def mqtt_subscription_callback(topic, message):
    global table_state
    print (f'Topic {topic} received message {message}')
    msg = message.decode('utf-8')
    table_state = msg
    if table_state == 'OPEN':
        print("opening table")
        table_state = msg
    if table_state == 'CLOSED':
        print("closing table")
        table_state = msg
    drive_motor(table_state)
    mqtt_client.publish(pub_topic, table_state)

mqtt_client.set_callback(mqtt_subscription_callback)

def mqtt_connect():
    global next_ping_time 
    global pingresp_rcv_flag
    global mqtt_con_flag
    global lock

    while not mqtt_con_flag:
        print("trying to connect to mqtt server.")
        led.off()
        try:
            mqtt_client.connect()
            mqtt_client.subscribe(sub_topic)
            mqtt_con_flag = True
            pingresp_rcv_flag = True
            next_ping_time = time.time() + PING_INTERVAL
            lock = False
        except Exception as e:
            print("Error in mqtt connect: [Exception]  %s: %s" % (type(e).__name__, e))
        time.sleep(0.5)

        print("Connected and subscribed to mqtt")
    led.on()
    
def ping_reset():
    global next_ping_time
    next_ping_time = time.time() + PING_INTERVAL
    print("Next MQTT ping at", next_ping_time)

def ping():
    mqtt_client.ping()
    ping_reset()

def check():
    global next_ping_time
    global mqtt_con_flag
    global pingresp_rcv_flag
    if (time.time() >= next_ping_time):
        ping()
    mqtt_client.check_msg()
    check_button_state(button.value())
    
def check_button_state(button_pressed):
    global table_state
    global offline
    
    if button_pressed:
        table_state = "OPEN"
        print("opening table")
    elif button_pressed:
        table_state = "CLOSED"
    drive_motor(table_state)
    if not offline:
        mqtt_client.publish(pub_topic, table_state)
    
    
while True:
    if not offline:
        try:
            mqtt_connect()
            check()
        except Exception as e:
            print("Error: [Exception] %s: %s" % (type(e).__name__, e))
            lock = True
            mqtt_con_flag = False
            raise e
    else:
        check_button_state(button.value())
        
    time.sleep(.1)
