from machine import Pin, SoftI2C
import time

led_pin = 2
led = Pin(led_pin, Pin.OUT)  

ADS1115_address = b"0x90"


def iic_init():

    i2c = SoftI2C(scl=Pin(22), sda=Pin(23), freq=400000)

    a = i2c.scan()
    led.value(a)
    i2c.write(ADS1115_address)
    
    #i2c.writeto(address, data, False)

iic_init()

while 1:
    #led.value(1)  
    time.sleep(0.5)
    #led.value(0) 
    time.sleep(0.5)