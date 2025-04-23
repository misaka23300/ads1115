from machine import Pin, I2C
import time

# 初始化一个GPIO引脚（与ADS1115无关的示例）
p12 = Pin(12, Pin.OUT)
p12.value(1)

# 初始化I2C总线
i2c = I2C(0, scl=Pin(22), sda=Pin(23), freq=400000)  # ESP32典型引脚

# ADS1115默认I2C地址
ADS1115_ADDR = 0x48

# 寄存器地址（直接使用整数，非字节数组）
REG_CONVERT = 0x00  # 转换结果寄存器
REG_CONFIG  = 0x01   # 配置寄存器

# 配置参数（单次转换模式+AIN0+±4.096V+128SPS）
# 高字节: 0x85 (单次转换|AIN0|±4.096V)
# 低字节: 0xE3 (128SPS|传统比较器模式)

#1000010111100011

# 放大倍数 6.144
#1 100 000 0 111 0 0 0 11 
# 1100 0000 1110 0011

# 通道0最快转换
# 1 100 000 0 111 0 0 0 11 
# 1100 0000 1110 0011
# -> 0xC0E3

config = bytearray([0xC0, 0xE3])

def ads1115_write_config():
    """写入配置寄存器"""
    # 组合成完整消息：[寄存器地址] + [配置高字节] + [配置低字节]
    buf = bytearray([REG_CONFIG]) + config
    i2c.writeto(ADS1115_ADDR, buf)

def ads1115_read():
    """读取ADC值 16位有符号整数"""
    # 启动单次转换
    ads1115_write_config()
    
    # 等待转换完成（128SPS约需8ms）
    time.sleep(0.00163)  # 实际可缩短至8ms，这里保守用10ms
    
    # 读取转换结果
    i2c.writeto(ADS1115_ADDR, bytearray([REG_CONVERT]))  # 先指定寄存器
    raw = i2c.readfrom(ADS1115_ADDR, 2)  # 读取2字节
    
    # 组合为16位有符号整数
    value = (raw[0] << 8) | raw[1]
    if value >= 0x8000:  # 处理负数
        value -= 0x10000
    
    return value

# 主循环
while True:
    try:
        raw_value = ads1115_read()
        voltage = raw_value * 6.144 / 32768.0  # 转换为电压值
        
        # 打印结果（保留3位小数）
        print("原始值: {:6d} | 电压: {:.4f} V".format(raw_value, voltage))
    except:
        print()
    