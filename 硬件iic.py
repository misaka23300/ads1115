from machine import Pin, I2C
import time


p12 = Pin(12,Pin.OUT)
p12.value(1)


i2c = I2C(0, scl=Pin(22), sda=Pin(23), freq=400000)

# ADS1115 I2C 地址（默认一般是 0x48）
ADS1115_ADDR = 0x48

# 寄存器地址
REG_CONVERT = bytearray(0x00)  # 转换结果寄存器
REG_CONFIG = bytearray(0x01)   # 配置寄存器

# 配置寄存器内容：单端AIN0, ±4.096V, 连续模式, 128SPS
# 0x45E3 -> 高字节: 0x45, 低字节: 0xE3
# 说明：
# - OS=1（启动一次转换）
# - MUX=100（AIN0 对 GND）
# - PGA=001（±4.096V）
# - MODE=0（连续转换）
# - DR=100（128SPS）
# - COMP相关全部禁用

config = bytearray([0x55, 0xE3])

def ads1115_write_config():

    # 写入配置寄存器（0x01 + 2字节配置值）
    i2c.writeto(ADS1115_ADDR, REG_CONFIG, False)

    i2c.writeto(ADS1115_ADDR, config, True)

def ads1115_read():
    # 先告诉芯片我们要读的是转换寄存器（0x00）
    i2c.writeto(ADS1115_ADDR, REG_CONVERT, False)

    # 然后读取2字节
    raw = i2c.readfrom(ADS1115_ADDR, 2, True)

    # 组合成16位有符号整数
    result = (raw[0] << 8) | raw[1]
    #if result >= 0x8000:
        #result -= 0x10000

    return result

# 写入配置
ads1115_write_config()

# 连续读取
while True:
    value = ads1115_read()
    voltage = value * 4.096 / 32768  # 转换为电压（±4.096V量程）
    print("ADC值：{} -> 电压：{:.3f} V".format(value, voltage))
    time.sleep(1)
