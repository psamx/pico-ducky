# License : GPLv2.0
# copyright (c) 2023  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)
# Pico and Pico W board support


import supervisor


import time
import board
import gc
from duckyinpython import *
if(board.board_id == 'raspberry_pi_pico_w'):
    import wifi
    from webapp import *


# sleep at the start to allow the device to be recognized by the host computer
time.sleep(.5)

def startWiFi():
    import ipaddress
    # Get wifi details and more from a secrets.py file
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    print("Connect wifi")
    #wifi.radio.connect(secrets['ssid'],secrets['password'])
    wifi.radio.start_ap(secrets['ssid'],secrets['password'])

    HOST = repr(wifi.radio.ipv4_address_ap)
    PORT = 80        # Port to listen on
    print(HOST,PORT)

# turn off automatically reloading when files are written to the pico
#supervisor.disable_autoreload()
supervisor.runtime.autoreload = False

progStatus = False
progStatus = Pico.in_setup_mode()
print("progStatus", progStatus)
if(progStatus == False):
    print("Finding payload")
    # not in setup mode, inject the payload
    payload = Pico.selectPayload()
    print("Running ", payload)
    runScript(payload)
    print("Done")
else:
    print("Update your payload")

led_state = False

async def main_loop():

    button_task = asyncio.create_task(Pico.monitor_buttons())
    if(board.board_id == 'raspberry_pi_pico_w'):
        pico_led_task = asyncio.create_task(Pico.blink_pico_w_led())
        print("Starting Wifi")
        startWiFi()
        print("Starting Web Service")
        webservice_task = asyncio.create_task(startWebService())
        await asyncio.gather(pico_led_task, button_task, webservice_task)
    else:
        pico_led_task = asyncio.create_task(Pico.blink_pico_led(led))
        await asyncio.gather(pico_led_task, button_task)

asyncio.run(main_loop())
