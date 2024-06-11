import digitalio
from duckyinpython import *
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer
import board
from board import *
import asyncio

class Pico:

    #init button
    button1_pin = DigitalInOut(GP22) # defaults to input
    button1_pin.pull = Pull.UP      # turn on internal pull-up resistor
    button1 =  Debouncer(button1_pin)

    #init payload selection switch
    payload1Pin = digitalio.DigitalInOut(GP4)
    payload1Pin.switch_to_input(pull=digitalio.Pull.UP)
    payload2Pin = digitalio.DigitalInOut(GP5)
    payload2Pin.switch_to_input(pull=digitalio.Pull.UP)
    payload3Pin = digitalio.DigitalInOut(GP10)
    payload3Pin.switch_to_input(pull=digitalio.Pull.UP)
    payload4Pin = digitalio.DigitalInOut(GP11)
    payload4Pin.switch_to_input(pull=digitalio.Pull.UP)

    """ Wrapper to interact with Raspberry Pi Pico's board """
    if(board.board_id == 'raspberry_pi_pico'):
        led = pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)
    elif(board.board_id == 'raspberry_pi_pico_w'):
        led = digitalio.DigitalInOut(board.LED)
        led.switch_to_output()

    @staticmethod 
    async def led_pwm_up():
        for i in range(100):
            if i < 50:
                Pico.led.duty_cycle = int(i * 2 * 65535 / 100)  # Up
            #time.sleep(0.01)
            await asyncio.sleep(0.01)

    @staticmethod 
    async def led_pwm_down():
        for i in range(100):
            if i >= 50:
                Pico.led.duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)  # Down
            #time.sleep(0.01)
            await asyncio.sleep(0.01)

    @staticmethod
    async def blink_pico_led():
        """ Task to continiously blink board LED """
        led_state = False

        while True:
            if led_state:
                print("Turning LED on")
                await Pico.led_pwm_up()
                led_state = False
            else:
                print("Turning LED off")
                await Pico.led_pwm_down()
                led_state = True

            await asyncio.sleep(0)
    
    @staticmethod
    async def blink_pico_w_led():
        """ Task to continiously blink board LED """
        led_state = False
        while True:
            if led_state:
                print("Turning LED on")
                Pico.led.value = 1
                await asyncio.sleep(0.5)
                led_state = False
            else:
                print("Turning LED off")
                Pico.led.value = 0
                await asyncio.sleep(0.5)
                led_state = True

            await asyncio.sleep(0.5)


    @staticmethod
    async def blink_led():
        print("Blink")
        if(board.board_id == 'raspberry_pi_pico'):
            await Pico.blink_pico_led()
        elif(board.board_id == 'raspberry_pi_pico_w'):
            await Pico.blink_pico_w_led()

    @staticmethod
    async def monitor_buttons():
        print("starting monitor_buttons")
        button1Down = False
        while True:
            Pico.button1.update()

            button1Pushed = Pico.button1.fell
            button1Released = Pico.button1.rose
            button1Held = not Pico.button1.value

            if(button1Pushed):
                print("Button 1 pushed")
                button1Down = True
            if(button1Released):
                print("Button 1 released")
                if(button1Down):
                    print("push and released")

            if(button1Released):
                if(button1Down):
                    # Run selected payload
                    payload = Pico.selectPayload()
                    print("Running ", payload)
                    runScript(payload)
                    print("Done")
                button1Down = False

            await asyncio.sleep(0)

    @staticmethod 
    def in_setup_mode() -> bool:
        setup_pin = digitalio.DigitalInOut(GP0)
        setup_pin.switch_to_input(pull=digitalio.Pull.UP)

        # Pull UP is default true so invert it
        return not setup_pin.value

    @staticmethod
    def selectPayload() -> str:
        payload = "payload.dd"
        # check switch status
        # payload1 = GPIO4 to GND
        # payload2 = GPIO5 to GND
        # payload3 = GPIO10 to GND
        # payload4 = GPIO11 to GND
        payload1State = not Pico.payload1Pin.value
        payload2State = not Pico.payload2Pin.value
        payload3State = not Pico.payload3Pin.value
        payload4State = not Pico.payload4Pin.value

        if(payload1State == True):
            payload = "payload.dd"

        elif(payload2State == True):
            payload = "payload2.dd"

        elif(payload3State == True):
            payload = "payload3.dd"

        elif(payload4State == True):
            payload = "payload4.dd"

        else:
            # if all pins are high, then no switch is present
            # default to payload1
            payload = "payload.dd"

        return payload
