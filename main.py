# ************************
# Web Server in ESP32 using
# web sockets (wifi station) or (AP)
# open sokects for non delay speed communication
# when Socket is open data flow between server and client
# open web socket is used when we need a real time communication


import socket
import network
import machine
led = machine.Pin(2,machine.Pin.OUT)
led.on()

# ************************
# Configure the ESP32 wifi
# as STAtion mode.
'''
ssid = "Rassi Net-2.4G"
password = "Holyshit"

sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    #sta.connect('your wifi ssid', 'your wifi password')
    sta.connect(ssid,password)
    while not sta.isconnected():
        pass
print('network config:', sta.ifconfig())

'''

#********************************
# Configure the esp32 direct wifi
# Configure the ESP32 as an Access Point
ssid = 'Sam_Ap'
password = '12345678'

# Function to activate the Access Point
def activate_access_point():
    print('Activating Access Point...')
    ap = network.WLAN(network.AP_IF)  # Initialize the WLAN interface in AP mode
    ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)  # Set WPA2 security
    ap.active(True)  # Activate the AP mode

    while not ap.active():
        pass  # Wait until the AP mode is active

    print('Access Point Active')
    print('AP Config:', ap.ifconfig())  # Print the network configuration
    ip_address = ap.ifconfig()[0]
    return ap, ip_address

activate_access_point()
led.off()




# ************************
# Configure the socket connection
# over TCP/IP


# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80)) # specifies that the socket is reachable 
#                 by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

# ************************
# Function for creating the
# web page to be displayed
def web_page():
    if led.value()==1:
        led_state = 'ON'
        print('led is ON')
    elif led.value()==0:
        led_state = 'OFF'
        print('led is OFF')

    html_page = """   
      <html>   
      <head>   
       <meta content="width=device-width, initial-scale=1" name="viewport"></meta>   
      </head>   
      <body>   
        <center><h2>ESP32 Web Server in MicroPython </h2></center>   
        <center>   
         <form>   
          <button name="LED" type="submit" value="1"> LED ON </button>   
          <button name="LED" type="submit" value="0"> LED OFF </button>   
         </form>   
        </center>   
        <center><p>LED is now <strong>""" + led_state + """</strong>.</p></center>   
      </body>   
      </html>"""  
    return html_page   

while True:
    # Socket accept() 
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))
    
    # Socket receive()
    request=conn.recv(1024)
    print("")
    print("")
    print("Content %s" % str(request))

    # Socket send()
    request = str(request)
    led_on = request.find('/?LED=1')
    led_off = request.find('/?LED=0')
    if led_on == 6:
        print('LED ON')
        print(str(led_on))
        led.value(1)
    elif led_off == 6:
        print('LED OFF')
        print(str(led_off))
        led.value(0)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    
    # Socket close()
    conn.close()
