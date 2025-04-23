# ADS1115

# 地址



![QQ_1745223826783](C:\Users\laffey\AppData\Local\Temp\QQ_1745223826783.png)

测试实例中,将ADDR引脚连接GND,所以地址是1001 000x,16进制读取为0x90, 写入为0x91.

## 接线

esp32的iic可以在任意引脚.

- P22 -> SCL 
- P23 -> SDA

```py
from machine import Pin, I2C


i2c = I2C(1, scl=Pin(22), sda=Pin(23), freq=400000)
```

## 通信过程

### 读

![QQ_1745231458404](C:\Users\laffey\AppData\Local\Temp\QQ_1745231458404.png)

1. 主机发送起始信号

2. 主机发送数据地址和读写位	7+1

3. 等待从机应答

4. 主机发送地址指针寄存器

5. 等待从机应答

6. 主机发送停止信号

   

7. 主机发送开始信号

8. 主机发送从机地址

9. 等待从机应答

10. 主机读取高八位数字量

11. 等待总计应答

12. 主机读取第八位数字量

13. 等待从机应答

14. 主机发送停止信号

### 写

![QQ_1745232016883](C:\Users\laffey\AppData\Local\Temp\QQ_1745232016883.png)

1. 主机发送开始信号
2. 主机发送从机地址
3. 等待从机应答
4. 主机发送需要操作的寄存器
5. 等待从机应答
6. 主机发送配置数据高八位
7. 等待从机应答
8. 主机发送配置数据第八位
9. 等待从机应答
10. 主机发送停止信号

## 寄存器

ADS1115有4个寄存器,分别是:

1. conversion register -> 读
2. config register -> 读写
3. 两个设置的寄存器

```python
REG_conversion = b"0x00"
REG_config = b"0x01"
REG_L_thresh = b"0x02"
REG_H_thresh = b"0x03"
```

### config register

  #### **1. OS (Operational Status or Single-Shot Conversion Start)**

  - **Bit 15**: 这个位决定设备的操作状态或启动单次转换。
    - **写操作：**
      - `0b` : 无效
      - `1b` : 启动单次转换（当设备处于待机模式时）
    - **读操作：**
      - `0b` : 设备正在执行转换
      - `1b` : 设备没有执行转换

  #### **2. MUX[2:0] (Input Multiplexer Configuration)**

  - **Bit 14:12**: 设置输入多路复用器，选择输入通道。
    - 这些位在 ADS1113 和 ADS1114 中没有作用，它们始终使用 AINP = AIN0 和 AINN = AIN1。
    - 配置选项：
      - `000b` : AINP = AIN0，AINN = AIN1（默认）
      - `001b` : AINP = AIN0，AINN = AIN3
      - `010b` : AINP = AIN1，AINN = AIN3
      - `011b` : AINP = AIN2，AINN = AIN3
      - `100b` : AINP = AIN0，AINN = GND
      - `101b` : AINP = AIN1，AINN = GND
      - `110b` : AINP = AIN2，AINN = GND
      - `111b` : AINP = AIN3，AINN = GND

  #### **3. PGA[2:0] (Programmable Gain Amplifier Configuration)**

  - **Bit 11:9**: 设置可编程增益放大器（PGA）的增益值，影响输入信号的放大倍数。
    - 配置选项：
      - `000b` : FSR = ±6.144V
      - `001b` : FSR = ±4.096V
      - `010b` : FSR = ±2.048V（默认）
      - `011b` : FSR = ±1.024V
      - `100b` : FSR = ±0.512V
      - `101b` : FSR = ±0.256V
      - `110b` : FSR = ±0.256V
      - `111b` : FSR = ±0.256V

  #### **4. MODE (Device Operating Mode)**

  - **Bit 8**: 控制设备的工作模式。
    - `0b` : 连续转换模式
    - `1b` : 单次转换模式或待机状态（默认）

  #### **5. DR[2:0] (Data Rate)**

  - **Bit 7:5**: 设置数据采样速率（Data Rate），影响数据转换速度。
    - 配置选项：
      - `000b` : 8 SPS
      - `001b` : 16 SPS
      - `010b` : 32 SPS
      - `011b` : 64 SPS
      - `100b` : 128 SPS（默认）
      - `101b` : 250 SPS
      - `110b` : 475 SPS
      - `111b` : 860 SPS

  #### **6. COMP_MODE (Comparator Mode)**

  - **Bit 4**: 配置比较器的工作模式。
    - `0b` : 传统比较器（默认）
    - `1b` : 窗口比较器（Window Comparator）

  #### **7. COMP_POL (Comparator Polarity)**

  - **Bit 3**: 控制 ALERT/RDY 引脚的极性。
    - `0b` : 活跃低（默认）
    - `1b` : 活跃高

  #### **8. COMP_LAT (Latching Comparator)**

  - **Bit 2**: 控制 ALERT/RDY 引脚是否锁存。
    - `0b` : 非锁存比较器（ALERT/RDY 引脚在转换后清除，默认）
    - `1b` : 锁存比较器（ALERT/RDY 引脚保持锁存，直到读取转换数据或响应 SMBus 警报）

  #### **9. COMP_QUE[1:0] (Comparator Queue and Disable)**

  - **Bit 1:0**: 配置比较器队列和禁用模式。
    - 这些位还可以控制 ALERT/RDY 引脚的高阻态。
    - 配置选项：
      - `00b` : 在一次转换后触发
      - `01b` : 在两次转换后触发
      - `10b` : 在四次转换后触发
      - `11b` : 禁用比较器并将 ALERT/RDY 引脚设置为高阻态（默认）

  ### **总结**

  `Configuration Register` 的各个字段对 ADS1115 的工作模式、增益、输入通道、采样速率以及比较器的行为进行了详细配置。正确配置这些字段可以优化设备的精度、响应速度和功耗，满足不同应用的需求。

  ### 参考配置

读：0 100 010 1 100 0 0 0 11

0100 0101 1110 0011 -> 45E3



## micropython写入代码

