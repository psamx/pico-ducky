# License : GPLv2.0
# copyright (c) 2023  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)
# Pico and Pico W board support


import supervisor
import time
import board
import asyncio
from duckyinpython import *
from pico import *
if(board.board_id == 'raspberry_pi_pico_w'):
    import wifi
    from webapp import *
    from dns import *


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
    while True:
        tasks = []
        try:
            button_task = asyncio.create_task(Pico.monitor_buttons())
            tasks.append(button_task)
            if board.board_id == 'raspberry_pi_pico_w':
                pico_led_task = asyncio.create_task(Pico.blink_pico_w_led())
                tasks.append(pico_led_task)
                print("Starting Wifi")
                startWiFi()
                print("Starting Web Service")
                webservice_task = asyncio.create_task(startWebService())
                tasks.append(webservice_task)
                print("Starting DNS server")
                dns_task = asyncio.create_task(run_dns_server(f'{wifi.radio.ipv4_address_ap}'))
                tasks.append(dns_task)
            else:
                pico_led_task = asyncio.create_task(Pico.blink_pico_led(led))
                tasks.append(pico_led_task)

            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"Error: {e}")
            print("Stopping remaining tasks and restarting main loop in 5 seconds...")
            for task in tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.sleep(5)

asyncio.run(main_loop())