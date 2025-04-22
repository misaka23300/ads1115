import time
from machine import Pin

led_pin = 2

def main():
    print("Welcome to RT-Thread MicroPython!")
    led = Pin(led_pin, Pin.OUT)  
    
    while True:
        led.value(1)  
        time.sleep(0.5)
        led.value(0) 
        time.sleep(0.5)
    
if __name__ == '__main__':
    main()








# 从地址0x3a的设备读取4个字节
#data = i2c.readfrom(0x3a, 4)
#print("读取到的数据:", data)

# 向地址0x3a的设备写入数据
#i2c.writeto(0x3a, bytearray([0x12]))  # 使用bytearray写入数据

# 创建一个10字节的缓冲区并写入设备
#buf = bytearray(10)  # 创建一个包含10个字节的缓冲区，默认初始化为0
#i2c.writeto(0x3a, buf)  # 将缓冲区数据写入设备




# 配置 I2C（SDA 和 SCL 根据实际连接的引脚调整）
#i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # 这里使用的是 SCL=22 和 SDA=21

# ADS1115 I2C 地址




