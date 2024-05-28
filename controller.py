import time
from machine import Pin
import network
from umqtt.simple import MQTTClient

led = machine.Pin("LED", machine.Pin.OUT)
in1 = machine.Pin(16, machine.Pin.OUT)
in2 = machine.Pin(17, machine.Pin.OUT)
in3 = machine.Pin(14, machine.Pin.OUT)
in4 = machine.Pin(15, machine.Pin.OUT)

# connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("{wifi_network}", "{wifi_password}")
while not wlan.isconnected():
    print("Connecting...")
    time.sleep(1)
print("Connected!")
# mqtt vars
mqtt_server = '{mqtt_server}'
mqtt_user = '{mqtt_user}'
mqtt_password = '{mqtt_password}'
client_id = 'table_motor_switch'
sub_topic = 'cmd/table_motor_switch'
pub_topic = 'state/table_motor_switch'
mqtt_status_topic = 'state/table_motor_switch/status'
PING_INTERVAL = 60
mqtt_con_flag = False
pingresp_rcv_flag = True
lock = True
next_ping_time = 0

table_state = ""

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
        in3.high()
        in4.low()
    if state == 'CLOSED':
        in1.low()
        in2.high()
        in3.low()
        in4.high()
    for i in range(6):
        led.toggle()
        time.sleep(0.1)

def mqtt_subscription_callback(topic, message):
    global table_state
    print (f'Topic {topic} received message {message}')
    msg = message.decode('utf-8')
    table_state = msg
    if table_state == 'OPEN':
        print("opening table")
        table_state = msg
        drive_motor(table_state)
    if table_state == 'CLOSED':
        print("closing table")
        table_state = msg
        drive_motor(table_state)
    mqtt_client.publish(pub_topic, table_state, retain=True)

mqtt_client.set_last_will(mqtt_status_topic, "disconnected", retain=True)
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
            mqtt_client.publish(mqtt_status_topic, "connected", retain=True)
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
    
while True:
    mqtt_connect()
    try:
        check()
    except Exception as e:
        print("Error: [Exception] %s: %s" % (type(e).__name__, e))
        lock = True
        mqtt_con_flag = False
        raise e
    time.sleep(.1)
