import numpy as np
import can

class RmdX8:
    def __init__(self):
        self.RMD_X8_SPEED_LIMITED = 514
        self.SET_TORQUE_CMD = "ST"
        self.m_rmd_x8_position = 0
        self.m_motor_torque = 0
        self.scale = 1 # unknown

    def cmd_send(self, cmd, Iq): # data = np.uint16(value)
        if cmd == self.SET_TORQUE_CMD:
            print("Set torque for motor run")
            self.m_motor_torque = Iq * self.scale
            data = [0xA1, 0x00, 0x00, 0x00, Iq & 0xFF, Iq >> 8, 0x00, 0x00]
            self.send_one(data)

    def send_one(self, data=None):
        if data is None:
            data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        with can.interface.Bus() as bus:
            msg = can.Message(
                arbitration_id=0x141, data=data, is_extended_id=False
            )

            try:
                bus.send(msg)
                print(f"Message sent on {bus.channel_info}")
            except can.CanError:
                print("Message NOT sent")
