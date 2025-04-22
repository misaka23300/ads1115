from machine import Pin, I2C

ads1115 = I2C(0, scl = Pin(22), sda = Pin(23), freq = 400000)

a = ads1115.scan()
print(a)

ADS1115_write_address = bytearray(0x90)
REG_config = bytearray(0x01)
config_data = bytearray([0x45, 0xE3])

def ads1115_write():

    # 写入从机地址
    ads1115.writeto(ADS1115_write_address, REG_config, 0)

    # 写入寄存器数据
    ads1115.writeto(ADS1115_write_address, config_data, 1)
    
def ads1115_read():
    
    ads1115.r


ads1115_write()

while 1:
    a = 0

