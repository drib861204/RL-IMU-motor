from OpenIMU_SPI import *
import matplotlib.pyplot as plt
import numpy as np
import time
import RPi.GPIO as GPIO

nRST_PIN = 21
time.sleep(0.1)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(nRST_PIN, GPIO.OUT)
time.sleep(0.1)
GPIO.output(nRST_PIN, 0)
time.sleep(5)
GPIO.output(nRST_PIN, 1)
print("Reset Ready")
time.sleep(0.1)

#object = RmdX8()
#object.cmd_send("ST", np.uint16(0))

#envs = Pendulum(0, 0)

ax = plt.axes()

openimu_spi = SpiOpenIMU(target_module="300ZI", fw='26.0.7', cs_pin = 19, interrupt_pin = 26, drdy_status=False)

read_name = [
            "X_Rate", "Y_Rate", "Z_Rate", "X_Accel", "Y_Accel", "Z_Accel", "RATE_TEMP", "BOARD_TEMP", "DRDY_RATE", "ACCEL_LPF", "ACCEL_SCALE_FACTOR", "RATE_SCALE_FACTOR", 
            "SN_1", "SN_2", "SN_3", "PRODUCT_ID", "MASTER_STATUS", "HW_STATUS", "SW_STATUS", "ACCEL_RANGE/RATE_RANGE", 
            "ORIENTATION_MSB/ORIENTATION_LSB", "SAVE_CONFIG", "RATE_LPF", "HW_VERSION/SW_VERSION"
            ]
read_reg = [
            0x04, 0x06, 0x08, 0x0A, 0x0C, 0x0E, 0x16, 0x18, 0x36, 0x38, 0x46, 0x47, 
            0x52, 0x54, 0x58, 0x56, 0x5A, 0x5C, 0x5E, 0x70, 0x74, 0x76, 0x78, 0x7E
            ]

t = []
log = []

#while True:
for _ in range(100000):
    '''cur_time = 0
    pre_time = 0
    dev = 0
    while True:
        if GPIO.event_detected(openimu_spi.interrupt_channel): 
            print("drdy fall")
            cur_time = time.clock()
            dev = cur_time-pre_time
            print(dev)
            pre_time = cur_time'''


    single = False
    read_degree = True
    if single:
        i = 15
        read_value = openimu_spi.single_read(read_reg[i])
        str_temp = "{0:_<40s}0x{1:<5X} read value: 0x{2:<10X}\n".format(read_name[i], read_reg[i], read_value)
        print(str_temp)

        time.sleep(1)
    else:
        if read_degree:
            list_rate, list_acc, list_deg = openimu_spi.burst_read(first_register=0x3D,subregister_num=11)
            str_burst = "time:{0:>10f};  gyro:{1:>25s};  accel:{2:>25s};  deg:{2:>25s} \n".format(
                time.clock(), ", ".join([str(x) for x in list_rate]), ", ".join([str(x) for x in list_acc]), ", ".join([str(x) for x in list_deg])
                )
            print(str_burst)
            q1 = list_deg[1]*100
            q1_dot = list_rate[1]
            '''if abs(q1)>1000:
                q1 = 0
            if abs(q1_dot)>1000:
                q1_dot = 0'''
        else:
            list_rate, list_acc = openimu_spi.burst_read(first_register=0x3E,subregister_num=11)
            str_burst = "time:{0:>10f};  gyro:{1:>25s};  accel:{2:>25s} \n".format(
                time.clock(), ", ".join([str(x) for x in list_rate]), ", ".join([str(x) for x in list_acc])
                )
            print(str_burst)

    ax.plot(time.clock(), q1, 'bo')
    ax.plot(time.clock(), q1_dot, 'r*')
    plt.draw()
    plt.pause(0.005)
    time.sleep(0.005)

